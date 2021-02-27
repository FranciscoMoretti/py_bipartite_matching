# -*- coding: utf-8 -*-
"""Contains classes and functions related to bipartite graphs.

The `BipartiteGraph` class is used to represent a bipartite graph as a dictionary. In particular,
`BipartiteGraph.find_matching()` can be used to find a maximum matching in such a graph.
"""

from typing import (Dict, Generic, Hashable, Iterator, List, Set, Tuple, TypeVar, Union, cast, MutableMapping)

from py_bipartite_matching.matching.hopcroft_karp import HopcroftKarp

try:
    from graphviz import Digraph, Graph
except ImportError:
    Digraph = Graph = None

__all__ = ['BipartiteGraph', 'DirectedMatchGraph']

T = TypeVar('T')
TLeft = TypeVar('TLeft', bound=Hashable)
TRight = TypeVar('TRight', bound=Hashable)
TEdgeValue = TypeVar('TEdgeValue')

Node = Tuple[int, Union[TLeft, TRight]]
NodeList = List[Node]
NodeSet = Set[Node]
Edge = Tuple[TLeft, TRight]

LEFT = 0
RIGHT = 1


class BipartiteGraph(Generic[TLeft, TRight, TEdgeValue], MutableMapping[Tuple[TLeft, TRight], TEdgeValue]):
    """A bipartite graph representation.

    This class is a specialized dictionary, where each edge is represented by a 2-tuple that is used as a key in the
    dictionary. The value can either be `True` or any value that you want to associate with the edge.

    For example, the edge from 1 to 2 with a label 42 would be set like this:

    >>> graph = BipartiteGraph()
    >>> graph[1, 2] = 42
    """

    __slots__ = ('_edges', '_left', '_right', '_graph')

    def __init__(self, *args, **kwargs):
        self._edges = dict(*args, **kwargs)
        self._left = set(l for (l, _) in self._edges.keys())
        self._right = set(r for (_, r) in self._edges.keys())
        self._graph = {}
        for l, r in self._edges:
            self._graph.setdefault((LEFT, l), set()).add((RIGHT, r))
            self._graph.setdefault((RIGHT, r), set()).add((LEFT, l))

    def __setitem__(self, key: Edge, value: TEdgeValue) -> None:
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("The edge must be a 2-tuple")
        self._edges.__setitem__(key, value)
        self._left.add(key[0])
        self._right.add(key[1])
        self._graph.setdefault((LEFT, key[0]), set()).add((RIGHT, key[1]))
        self._graph.setdefault((RIGHT, key[1]), set()).add((LEFT, key[0]))

    def __getitem__(self, key: Edge) -> TEdgeValue:
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("The edge must be a 2-tuple")
        return self._edges.__getitem__(key)

    def __delitem__(self, key: Edge) -> None:
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("The edge must be a 2-tuple")
        self._edges.__delitem__(key)
        if all(l != key[0] for (l, _) in self._edges):
            self._left.remove(key[0])
        if all(r != key[1] for (_, r) in self._edges):
            self._right.remove(key[1])
        self._graph[(LEFT, key[0])].remove((RIGHT, key[1]))
        self._graph[(RIGHT, key[1])].remove((LEFT, key[0]))

    def edges_with_labels(self):
        """Returns a view on the edges with labels."""
        return self._edges.items()

    def edges(self):
        return self._edges.keys()

    def clear(self):
        """Removes all cached data."""
        self._edges.clear()
        self._left.clear()
        self._right.clear()
        self._graph.clear()

    def __copy__(self):
        new_graph = type(self)()
        new_graph._edges = self._edges.copy()
        new_graph._left = self._left.copy()
        new_graph._right = self._right.copy()
        new_graph._graph = self._graph.copy()
        return new_graph

    def __iter__(self):
        return self._edges.__iter__()

    def __len__(self):
        return self._edges.__len__()

    def __eq__(self, other):
        if isinstance(other, dict):
            return self._edges == other
        elif isinstance(self, type(other)):
            return self._edges == other._edges
        else:
            return NotImplemented

    def as_graph(self) -> Graph:  # pragma: no cover
        """Returns a :class:`graphviz.Graph` representation of this bipartite graph."""
        if Graph is None:
            raise ImportError('The graphviz package is required to draw the graph.')
        graph = Graph()
        nodes_left = {}  # type: Dict[TLeft, str]
        nodes_right = {}  # type: Dict[TRight, str]
        node_id = 0
        for (left, right), value in self._edges.items():
            if left not in nodes_left:
                name = 'node{:d}'.format(node_id)
                nodes_left[left] = name
                graph.node(name, label=str(left))
                node_id += 1
            if right not in nodes_right:
                name = 'node{:d}'.format(node_id)
                nodes_right[right] = name
                graph.node(name, label=str(right))
                node_id += 1
            edge_label = value is not True and str(value) or ''
            graph.edge(nodes_left[left], nodes_right[right], edge_label)
        return graph

    def find_matching(self) -> Dict[TLeft, TRight]:
        """Finds a matching in the bipartite graph.

        This is done using the Hopcroft-Karp algorithm.

        Returns:
            A dictionary where each edge of the matching is represented by a key-value pair
            with the key being from the left part of the graph and the value from te right part.
        """
        # The directed graph is represented as a dictionary of edges
        # The key is the tail of all edges which are represented by the value
        # The value is a set of heads for the all edges originating from the tail (key)
        # In addition, the graph stores which part of the bipartite graph a node originated from
        # to avoid problems when a value exists in both halfs.
        # Only one direction of the undirected edge is needed for the HopcroftKarp class
        directed_graph = {}  # type: Dict[Tuple[int, TLeft], List[Tuple[int, TRight]]]

        for (left, right) in self._edges:
            tail = (LEFT, left)
            head = (RIGHT, right)
            if tail not in directed_graph:
                directed_graph[tail] = [head]
            else:
                directed_graph[tail].append(head)

        matching = HopcroftKarp(directed_graph).get_maximum_matching()

        # Filter out the partitions (LEFT and RIGHT) and only return the matching edges
        # that go from LEFT to RIGHT
        return dict((tail[1], head[1]) for tail, head in matching.items() if tail[0] == LEFT)


    def _find_cycle(self, node: Node , path: NodeList, visited: NodeSet) -> NodeList: 
        """
        A recursive function that uses visited[] and parent to detect 
        cycle in subgraph reachable from a node. 
        """
        if node in visited:
            try:
                index = path.index(node)
                return path[index:]
            except ValueError:
                return cast(NodeList, [])

        visited.add(node)

        if node not in self._graph:
            return cast(NodeList, [])

        # Recur for all the vertices adjacent to this vertex 
        for other in self._graph[node]:
            if len(path) == 0 or path[-1] != other:
                # If the node is not visited then recurse on it 
                cycle = self._find_cycle(other, path + [node], visited)
                if cycle:
                    return cycle

        return cast(NodeList, [])
           
    def find_cycle(self) -> NodeList: 
        """Returns true if the graph contains a cycle, else false."""
        # Initialize the visited set 
        visited = cast(NodeSet, set())
        # Call the recursive helper function to detect cycle in different DFS trees 
        for n in self._graph.keys(): 
            # Don't recur if it is already visited 
            cycle = self._find_cycle(n, cast(NodeList, []), visited)   
            if cycle: 
                return cycle
        return cast(NodeList, [])

    def without_nodes(self, edge: Edge) -> 'BipartiteGraph[TLeft, TRight, TEdgeValue]':
        """Returns a copy of this bipartite graph with the given edge and its adjacent nodes removed."""
        return BipartiteGraph(((n1, n2), v) for (n1, n2), v in self._edges.items() if n1 != edge[0] and n2 != edge[1])

    def without_edge(self, edge: Edge) -> 'BipartiteGraph[TLeft, TRight, TEdgeValue]':
        """Returns a copy of this bipartite graph with the given edge removed."""
        return BipartiteGraph((e2, v) for e2, v in self._edges.items() if edge != e2)

    def limited_to(self, left: Set[TLeft], right: Set[TRight]) -> 'BipartiteGraph[TLeft, TRight, TEdgeValue]':
        """Returns the induced subgraph where only the nodes from the given sets are included."""
        return BipartiteGraph(((n1, n2), v) for (n1, n2), v in self._edges.items() if n1 in left and n2 in right)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._edges)


class DirectedMatchGraph(Dict[Node, NodeSet], Generic[TLeft, TRight]):
    def __init__(self, graph: BipartiteGraph[TLeft, TRight, TEdgeValue], matching: Dict[TLeft, TRight]) -> None:
        super(DirectedMatchGraph, self).__init__()
        for (tail, head) in graph:
            if tail in matching and matching[tail] == head:
                self[(LEFT, tail)] = {(RIGHT, head)}
            else:
                if (RIGHT, head) not in self:
                    self[(RIGHT, head)] = set()
                self[(RIGHT, head)].add((LEFT, tail))

    def as_graph(self) -> Digraph:  # pragma: no cover
        """Returns a :class:`graphviz.Digraph` representation of this directed match graph."""
        if Digraph is None:
            raise ImportError('The graphviz package is required to draw the graph.')
        graph = Digraph()

        subgraphs = [Digraph(graph_attr={'rank': 'same'}), Digraph(graph_attr={'rank': 'same'})]
        nodes = [{}, {}]  # type: List[Dict[Union[TLeft, TRight], str]]
        edges = []  # type: List [Tuple[str, str]]
        node_id = 0
        for (tail_part, tail), head_set in self.items():
            if tail not in nodes[tail_part]:
                name = 'node{:d}'.format(node_id)
                nodes[tail_part][tail] = name
                subgraphs[tail_part].node(name, label=str(tail))
                node_id += 1
            for head_part, head in head_set:
                if head not in nodes[head_part]:
                    name = 'node{:d}'.format(node_id)
                    nodes[head_part][head] = name
                    subgraphs[head_part].node(name, label=str(head))
                    node_id += 1
                edges.append((nodes[tail_part][tail], nodes[head_part][head]))
        graph.subgraph(subgraphs[0])
        graph.subgraph(subgraphs[1])
        for tail_node, head_node in edges:
            graph.edge(tail_node, head_node)
        return graph

    def find_cycle(self) -> NodeList:
        visited = cast(NodeSet, set())
        for n in self:
            cycle = self._find_cycle(n, cast(NodeList, []), visited)
            if cycle:
                return cycle
        return cast(NodeList, [])

    def _find_cycle(self, node: Node, path: NodeList, visited: NodeSet) -> NodeList:
        if node in visited:
            try:
                index = path.index(node)
                return path[index:]
            except ValueError:
                return cast(NodeList, [])

        visited.add(node)

        if node not in self:
            return cast(NodeList, [])

        for other in self[node]:
            cycle = self._find_cycle(other, path + [node], visited)
            if cycle:
                return cycle

        return cast(NodeList, [])

