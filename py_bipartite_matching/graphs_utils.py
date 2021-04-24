# utils for graphs of the networkx library
import copy
import networkx as nx
from networkx.algorithms.shortest_paths import shortest_path
from typing import Any, Union, Optional, Iterator, Iterable, Tuple, Dict, List, cast

LEFT = 0
RIGHT = 1


def top_nodes(graph: nx.Graph,
              data: bool = False) -> Union[Iterator[Any], Iterator[Tuple[Any, Any]]]:
    for node_id, node_data in graph.nodes(data=True).__iter__():
        if node_data['bipartite'] == 0:
            if data:
                yield node_id, node_data
            else:
                yield node_id


def bottom_nodes(graph: nx.Graph,
                 data: bool = False) -> Union[Iterator[Any], Iterator[Tuple[Any, Any]]]:
    for node_id, node_data in graph.nodes(data=True).__iter__():
        if node_data['bipartite'] == 1:
            if data:
                yield node_id, node_data
            else:
                yield node_id


def bipartite_node_positions(graph: nx.Graph) -> Dict[int, Tuple[int, int]]:
    pos: Dict[int, Tuple[int, int]] = dict()
    pos.update((n, (1, i)) for i, n in enumerate(top_nodes(graph)))  # put nodes from X at x=1
    pos.update((n, (2, i)) for i, n in enumerate(bottom_nodes(graph)))  # put nodes from Y at x=2
    return pos


def draw_bipartite(graph: nx.Graph) -> None:
    pos = bipartite_node_positions(graph)
    nx.draw(graph, pos=pos, with_labels=True, font_weight='bold')


def draw_nodes(graph: nx.Graph, labels: bool = False) -> None:
    pos = bipartite_node_positions(graph)
    nx.draw_networkx_nodes(graph, pos=pos, node_size=300)
    if labels:
        top_node_labels = {k: str(v['label']) for k, v in tuple(top_nodes(graph, data=True))}
        nx.draw_networkx_labels(graph, pos=pos, labels=top_node_labels, horizontalalignment='left')
        bottom_node_labels = {k: str(v['label']) for k, v in tuple(bottom_nodes(graph, data=True))}
        nx.draw_networkx_labels(graph,
                                pos=pos,
                                labels=bottom_node_labels,
                                horizontalalignment='right')
    else:
        nx.draw_networkx_labels(graph, pos=pos)


def draw_edges(graph: nx.Graph, edge_list: Optional[Iterable[Tuple[Any, Any]]] = None) -> None:
    pos = bipartite_node_positions(graph)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=edge_list)


def draw_matching(graph: nx.Graph, matching: Dict[Any, Any], labels: bool = False) -> None:
    draw_nodes(graph, labels=labels)
    draw_edges(graph, matching.items())


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


def find_feasible_two_edge_path(graph: nx.Graph,
                                matching: Dict[Any, Any]) -> Optional[Tuple[Any, Any, Any]]:
    # This path has the form top1 -> bottom -> top2 or bottom1 -> top -> bottom2
    # first: must be in the left part of the graph and in matching
    # second: must be in the right part of the graph and in matching
    # third: is also in the left part of the graph and but must not be in matching

    for top, bottom in matching.items():
        if top in top_nodes(graph) and bottom in bottom_nodes(graph):
            for new_bottom in graph.neighbors(top):
                if new_bottom not in matching.values():
                    return (bottom, top, new_bottom)
            for new_top in graph.neighbors(bottom):
                if new_top not in matching:
                    return (top, bottom, new_top)
    return None


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


def create_directed_matching_graph(graph: nx.Graph, top_nodes: Iterable[Any],
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