# utils for graphs of the networkx library
import copy
import networkx as nx
from networkx.algorithms.shortest_paths import shortest_path
from typing import Any, Tuple, Dict, List, Set, cast


def find_cycle_with_edge_of_matching(graph: nx.Graph, matching: Dict[Any, Any]) -> List[Any]:
    tmp_graph = copy.deepcopy(graph)
    # Remove the edge so and find a path from a node of the edge to the other one.
    # If a path is found, the circle is completed with the removed edge
    for k, v in matching.items():
        if not tmp_graph.has_edge(k, v):
            # The graph could have been reduced
            continue
        tmp_graph.remove_edge(k, v)
        try:
            path = shortest_path(G=tmp_graph, source=v, target=k)
        except nx.NetworkXNoPath:
            tmp_graph.add_edge(k, v)
            continue
        else:
            tmp_graph.add_edge(k, v)
            return cast(List[Any], path)
    # No cycle was found
    raise nx.NetworkXNoCycle


def strongly_connected_components_decomposition(graph: nx.DiGraph) -> nx.DiGraph:
    scc = nx.strongly_connected_components(graph)
    for cc in scc:
        for node in cc:
            to_remove = set()
            for neighbor in graph.adj[node]:
                if neighbor not in cc:
                    to_remove.add(neighbor)
            for neighbor in to_remove:
                graph.remove_edge(node, neighbor)
    return graph


def create_directed_matching_graph(graph: nx.Graph, top_nodes: Set[Any],
                                   matching: Dict[Any, Any]) -> nx.DiGraph:
    # creates a directed copy of the graph with all edges on both directions
    directed_graph = graph.to_directed()

    for top_node in top_nodes:
        for bottom_node in graph.adj[top_node]:
            if top_node in matching.keys() and bottom_node == matching[top_node]:
                directed_graph.remove_edge(bottom_node, top_node)
            else:
                directed_graph.remove_edge(top_node, bottom_node)
    # check for duplicated (should not exist any)
    ordered_edges = [tuple(sorted(e)) for e in directed_graph.edges]
    assert len(ordered_edges) == len(set(ordered_edges))

    assert len(graph.edges) == len(directed_graph.edges)
    assert len(graph.nodes) == len(directed_graph.nodes)

    return directed_graph


def graph_without_nodes_of_edge(graph: nx.Graph, edge: Tuple[Any, Any]) -> nx.Graph:
    """Returns a copy of this bipartite graph with the given edge and its adjacent nodes removed."""
    new_graph = copy.deepcopy(graph)

    if new_graph.graph.get('top') and new_graph.graph.get('bottom'):
        if edge[0] in new_graph.graph.get('top'):
            new_graph.graph.get('top').remove(edge[0])
            new_graph.graph.get('bottom').remove(edge[1])
        else:
            new_graph.graph.get('top').remove(edge[1])
            new_graph.graph.get('bottom').remove(edge[0])
        assert len(new_graph.graph.get('top')) == len(graph.graph.get('top')) - 1
        assert len(new_graph.graph.get('bottom')) == len(graph.graph.get('bottom')) - 1

    new_graph.remove_node(edge[0])
    new_graph.remove_node(edge[1])
    assert new_graph != graph
    assert len(new_graph.nodes) == len(graph.nodes) - 2
    return new_graph


def graph_without_edge(graph: nx.Graph, edge: Tuple[Any, Any]) -> nx.Graph:
    """Returns a copy of this bipartite graph with the given edge removed."""
    new_graph = copy.deepcopy(graph)
    new_graph.remove_edge(*edge)

    assert len(new_graph.edges) == len(graph.edges) - 1
    assert len(new_graph.nodes) == len(graph.nodes)
    return new_graph