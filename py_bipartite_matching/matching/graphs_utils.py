# utils for graphs of the networkx library
import copy
import networkx as nx


def graph_without_nodes_of_edge(graph, edge):
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


def graph_without_edge(graph, edge):
    """Returns a copy of this bipartite graph with the given edge removed."""
    new_graph = copy.deepcopy(graph)
    new_graph.remove_edge(*edge)

    assert len(new_graph.edges) == len(graph.edges) - 1
    assert len(new_graph.nodes) == len(graph.nodes)
    return new_graph