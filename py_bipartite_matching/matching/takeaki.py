# -*- coding: utf-8 -*-
"""Contains classes and functions related to Algorithms for Enumerating All Perfect,
Maximum and Maximal Matchings in Bipartite Graphs. From Takeaki Uno publication.

The function `enum_perfect_matchings` can be used to enumerate all maximum matchings of a `BipartiteGraph`.
The function `enum_maximum_matchings` can be used to enumerate all maximum matchings of a `BipartiteGraph`.
"""
from typing import (Dict, Generic, Hashable, Iterator, List, Set, Tuple, TypeVar, Union, cast, MutableMapping)

from py_bipartite_matching.matching.bipartite import (
    BipartiteGraph,
    _DirectedMatchGraph,
    T,
    TLeft,
    TRight,
    TEdgeValue,
    Node,
    NodeList,
    NodeSet,
    Edge,
    LEFT,
    RIGHT
)

__all__ = ['enum_perfect_matchings', 'enum_maximum_matchings'] 


def enum_perfect_matchings(graph: BipartiteGraph[TLeft, TRight, TEdgeValue]) -> Iterator[Dict[TLeft, TRight]]:
    if len(graph._left) != len(graph._right):
        return
    size = len(graph._left)
    matching = graph.find_matching()
    if matching and len(matching) == size:
        yield matching
        graph = graph.__copy__()
        yield from _enum_perfect_matchings_iter(graph, matching)


def _enum_perfect_matchings_iter(graph: BipartiteGraph[TLeft, TRight, TEdgeValue], matching: Dict[TLeft, TRight]) \
    -> Iterator[Dict[TLeft, TRight]]:
    # Algorithm described in "Algorithms for Enumerating All Perfect, Maximum and Maximal Matchings in Bipartite Graphs"
    # By Takeaki Uno in "Algorithms and Computation: 8th International Symposium, ISAAC '97 Singapore,
    # December 17-19, 1997 Proceedings"
    # See http://dx.doi.org/10.1007/3-540-63890-3_11

    # Step 1
    if len(graph) == 0:
        return

    # Find a cycle in the directed matching graph
    # Note that this cycle alternates between nodes from the left and the right part of the graph

    # TODO: avoid doing a directed graph by implementing missing algorithm steps from paper
    directed_match_graph = _DirectedMatchGraph(graph, matching)
    raw_cycle = directed_match_graph.find_cycle()

    # raw_cycle = graph.find_cycle()

    if not raw_cycle:
        return

    # Make sure the cycle "starts"" in the the left part
    # If not, start the cycle from the second node, which is in the left part
    if raw_cycle[0][0] != LEFT:
        cycle = tuple([raw_cycle[-1][1]] + list(x[1] for x in raw_cycle[:-1]))
    else:
        cycle = tuple(x[1] for x in raw_cycle)

    # Step 2 - TODO: Properly find right edge? (to get complexity bound)
    edge = cast(Edge, cycle[:2])

    # Step 3
    # already done because we are not really finding the optimal edge

    # Step 4
    # Construct new matching M' by flipping edges along the cycle, i.e. change the direction of all the
    # edges in the cycle
    matching_prime = matching.copy()
    for i in range(0, len(cycle), 2):
        matching_prime[cycle[i]] = cycle[i - 1]  # type: ignore

    yield matching_prime

    # Construct G+(e)
    graph_plus = graph.without_nodes(edge)

    # Step 5
    # TODO: Trim unnecessary edges from G+(e).

    # Step 6
    # Recurse with the old matching M but without the edge e
    yield from _enum_perfect_matchings_iter(graph_plus, matching)

    # Construct G-(e)
    graph_minus = graph.without_edge(edge)

    # Step 7
    # Trim unnecessary edges from G-(e).
    
    # Step 8
    # Recurse with the new matching M' but without the edge e
    yield from _enum_perfect_matchings_iter(graph_minus, matching_prime)


def enum_maximum_matchings(graph: BipartiteGraph[TLeft, TRight, TEdgeValue]) -> Iterator[Dict[TLeft, TRight]]:
    matching = graph.find_matching()
    if matching:
        yield matching
        graph = graph.__copy__()
        yield from _enum_maximum_matchings_iter(graph, matching, _DirectedMatchGraph(graph, matching))


def _enum_maximum_matchings_iter(graph: BipartiteGraph[TLeft, TRight, TEdgeValue], matching: Dict[TLeft, TRight],
                                 directed_match_graph: _DirectedMatchGraph[TLeft, TRight]) \
        -> Iterator[Dict[TLeft, TRight]]:
    # Algorithm described in "Algorithms for Enumerating All Perfect, Maximum and Maximal Matchings in Bipartite Graphs"
    # By Takeaki Uno in "Algorithms and Computation: 8th International Symposium, ISAAC '97 Singapore,
    # December 17-19, 1997 Proceedings"
    # See http://dx.doi.org/10.1007/3-540-63890-3_11

    # Step 1
    if len(graph) == 0:
        return

    # Step 2
    # Find a cycle in the directed matching graph
    # Note that this cycle alternates between nodes from the left and the right part of the graph
    raw_cycle = directed_match_graph.find_cycle()

    if raw_cycle:
        # Make sure the cycle "starts"" in the the left part
        # If not, start the cycle from the second node, which is in the left part
        if raw_cycle[0][0] != LEFT:
            cycle = tuple([raw_cycle[-1][1]] + list(x[1] for x in raw_cycle[:-1]))
        else:
            cycle = tuple(x[1] for x in raw_cycle)

        # Step 3 - TODO: Properly find right edge? (to get complexity bound)
        edge = cast(Edge, cycle[:2])

        # Step 4
        # already done because we are not really finding the optimal edge

        # Step 5
        # Construct new matching M' by flipping edges along the cycle, i.e. change the direction of all the
        # edges in the cycle
        matching_prime = matching.copy()
        for i in range(0, len(cycle), 2):
            matching_prime[cycle[i]] = cycle[i - 1]  # type: ignore

        yield matching_prime

        # Step 6
        # Construct G+(e) and D(G+(e), M\e)
        graph_plus = graph.without_nodes(edge)
        directed_match_graph_plus = _DirectedMatchGraph(graph_plus, matching)
        # Recurse with the old matching M but without the edge e
        yield from _enum_maximum_matchings_iter(graph_plus, matching, directed_match_graph_plus)

        # Step 7
        # Construct G-(e) and D(G-(e), M')
        graph_minus = graph.without_edge(edge)
        directed_match_graph_minus = _DirectedMatchGraph(graph_minus, matching_prime)
        # Recurse with the new matching M' but without the edge e
        yield from _enum_maximum_matchings_iter(graph_minus, matching_prime, directed_match_graph_minus)

    else:
        # Step 8
        # Find feasible path of length 2 in D(graph, matching)
        # This path has the form left1 -> right -> left2
        # left1 must be in the left part of the graph and in matching
        # right must be in the right part of the graph
        # left2 is also in the left part of the graph and but must not be in matching
        left1 = None  # type: TLeft
        left2 = None  # type: TLeft
        right = None  # type: TRight

        for part1, node1 in directed_match_graph:
            if part1 == LEFT and node1 in matching:
                left1 = cast(TLeft, node1)
                right = matching[left1]
                if (RIGHT, right) in directed_match_graph:
                    for _, node2 in directed_match_graph[(RIGHT, right)]:
                        if node2 not in matching:
                            left2 = cast(TLeft, node2)
                            break
                    if left2 is not None:
                        break

        if left2 is None:
            return

        # Construct M'
        # Exchange the direction of the path left1 -> right -> left2
        # to left1 <- right <- left2 in the new matching
        matching_prime = matching.copy()
        del matching_prime[left1]
        matching_prime[left2] = right

        yield matching_prime

        edge = (left2, right)

        # Construct G+(e) and G-(e)
        graph_plus = graph.without_nodes(edge)
        graph_minus = graph.without_edge(edge)

        dgm_plus = _DirectedMatchGraph(graph_plus, matching_prime)
        dgm_minus = _DirectedMatchGraph(graph_minus, matching)

        # Step 9
        yield from _enum_maximum_matchings_iter(graph_plus, matching_prime, dgm_plus)

        # Step 10
        yield from _enum_maximum_matchings_iter(graph_minus, matching, dgm_minus)

