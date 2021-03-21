# -*- coding: utf-8 -*-
"""Contains classes and functions related to Algorithms for Enumerating All Perfect,
Maximum and Maximal Matchings in Bipartite Graphs. From Takeaki Uno publication.

The function `enum_perfect_matchings` can be used to enumerate all maximum matchings of a `BipartiteGraph`.
The function `enum_maximum_matchings` can be used to enumerate all maximum matchings of a `BipartiteGraph`.
"""
from typing import (Dict, Generic, Hashable, Iterator, List, Set, Tuple, TypeVar, Union, cast, MutableMapping)

import copy
import networkx as nx
from networkx.algorithms.bipartite.matching import maximum_matching

from py_bipartite_matching.matching.graphs_utils import (
    networkx_graph_without_edge,
    networkx_graph_without_nodes_of_edge
)

from py_bipartite_matching.matching.bipartite import (
    BipartiteGraph,
    DirectedMatchGraph,
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

__all__ = ['enum_perfect_matchings_networkx', 'enum_maximum_matchings_networkx', 'create_directed_matching_graph'] 


def create_directed_matching_graph(graph: nx.Graph, top_nodes: set, matching: dict) -> nx.DiGraph:
    # creates a directed copy of the graph with all edges on both directions
    directed_graph = graph.to_directed()

    for top_node in top_nodes:
        for bottom_node in graph.adj[top_node]:
            if top_node in matching.keys() and bottom_node in matching[top_node]:
                directed_graph.remove_edge(bottom_node, top_node)
            else:
                directed_graph.remove_edge(top_node, bottom_node)
    # check for duplicated (should not exist any)
    ordered_edges = [tuple(sorted(e)) for e in directed_graph.edges]
    assert len(ordered_edges) == len(set(ordered_edges))

    assert len(graph.edges) == len(directed_graph.edges) 
    assert len(graph.nodes) == len(directed_graph.nodes) 

    return directed_graph

def enum_perfect_matchings_networkx(graph: nx.Graph) -> Iterator[Dict[TLeft, TRight]]:
    if len(graph._left) != len(graph._right):
        return
    size = len(graph._left)
    matching = nx.maximum_matching(graph)
    if matching and len(matching) == size:
        yield matching
        graph = graph.__copy__()
        yield from _enum_perfect_matchings_iter_networkx(graph, matching)


def _enum_perfect_matchings_iter_networkx(graph: BipartiteGraph[TLeft, TRight, TEdgeValue], matching: Dict[TLeft, TRight]) \
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
    directed_match_graph = DirectedMatchGraph(graph, matching)
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
    yield from _enum_perfect_matchings_iter_networkx(graph_plus, matching)

    # Construct G-(e)
    graph_minus = graph.without_edge(edge)

    # Step 7
    # Trim unnecessary edges from G-(e).
    
    # Step 8
    # Recurse with the new matching M' but without the edge e
    yield from _enum_perfect_matchings_iter_networkx(graph_minus, matching_prime)


def enum_maximum_matchings_networkx(graph: nx.Graph) -> Iterator[dict]:
    matching = maximum_matching(graph, top_nodes=graph.graph['top'])
    # Express the matching only from a top node to a bottom node
    matching = {k: v for k, v in matching.items() if k in graph.graph['top']}
    if matching:
        yield matching
        yield from _enum_maximum_matchings_iter_networkx(
            graph=copy.deepcopy(graph),
            matching=matching,
            directed_match_graph=create_directed_matching_graph(graph, graph.graph['top'], matching))


def _enum_maximum_matchings_iter_networkx(graph: nx.Graph, matching: dict,
                                          directed_match_graph: nx.DiGraph) \
        -> Iterator[dict]:
    # Algorithm described in "Algorithms for Enumerating All Perfect, Maximum and Maximal Matchings in Bipartite Graphs"
    # By Takeaki Uno in "Algorithms and Computation: 8th International Symposium, ISAAC '97 Singapore,
    # December 17-19, 1997 Proceedings"
    # See http://dx.doi.org/10.1007/3-540-63890-3_11

    # Step 1
    if len(graph.nodes) == 0:
        return

    # Step 2
    # Find a cycle in the directed matching graph
    # Note that this cycle alternates between nodes from the left and the right part of the graph
    try:
        raw_cycle = nx.find_cycle(directed_match_graph)
        assert len(raw_cycle) > 3
    except nx.exception.NetworkXNoCycle:
        raw_cycle = None


    if raw_cycle:
        # Make sure the cycle "starts"" in the the left part
        # If not, start the cycle from the second node, which is in the left part
        if directed_match_graph.nodes[raw_cycle[0][0]]['bipartite'] == LEFT:
            cycle = tuple([raw_cycle[-1][1]] + list(x[1] for x in raw_cycle[:-1]))
        else:
            cycle = tuple(x[1] for x in raw_cycle)
        assert directed_match_graph.nodes[cycle[0]]['bipartite'] == LEFT
        # left0, right0, left1, right1

        # Step 3 - TODO: Properly find right edge? (to get complexity bound)
        edge = tuple(cycle[:2])

        # Step 4
        # already done because we are not really finding the optimal edge

        # Step 5
        # Construct new matching M' by flipping edges along the cycle, i.e. change the direction of all the
        # edges in the cycle
        matching_prime = matching.copy()
        for i in range(0, len(cycle), 2):
            matching_prime[cycle[i]] = cycle[i - 1]  # type: ignore
    
        assert matching_prime != matching
        yield matching_prime

        # Step 6
        # Construct G+(e) and D(G+(e), M\e)
        graph_plus = networkx_graph_without_nodes_of_edge(graph, edge)
        directed_match_graph_plus = create_directed_matching_graph(graph_plus, graph_plus.graph['top'], matching)
        # Recurse with the old matching M but without the edge e
        yield from _enum_maximum_matchings_iter_networkx(graph_plus, matching, directed_match_graph_plus)

        # Step 7
        # Construct G-(e) and D(G-(e), M')
        graph_minus = networkx_graph_without_edge(graph, edge)
        directed_match_graph_minus = create_directed_matching_graph(graph_minus, graph_minus.graph['top'], matching_prime)
        # Recurse with the new matching M' but without the edge e
        yield from _enum_maximum_matchings_iter_networkx(graph_minus, matching_prime, directed_match_graph_minus)

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

        for node1 in directed_match_graph.nodes:
            if directed_match_graph.nodes[node1]['bipartite'] == LEFT and node1 in matching.keys():
                left1 = node1
                right = matching[left1]
                if right in directed_match_graph.nodes:
                    for node2 in directed_match_graph.neighbors(right):
                        if node2 not in matching:
                            left2 = node2
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

        assert matching_prime != matching
        yield matching_prime

        edge = (left2, right)

        # Construct G+(e) and G-(e)
        graph_plus = networkx_graph_without_nodes_of_edge(graph, edge)
        graph_minus = networkx_graph_without_edge(graph, edge)

        dgm_plus = create_directed_matching_graph(graph_plus, graph_plus.graph['top'], matching_prime)
        dgm_minus = create_directed_matching_graph(graph_minus, graph_minus.graph['top'], matching)

        # Step 9
        yield from _enum_maximum_matchings_iter_networkx(graph_plus, matching_prime, dgm_plus)

        # Step 10
        yield from _enum_maximum_matchings_iter_networkx(graph_minus, matching, dgm_minus)

