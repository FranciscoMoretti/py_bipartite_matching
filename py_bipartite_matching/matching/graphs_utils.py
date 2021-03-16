# utils for graphs of the PyGraph library 
import copy
import networkx as nx
from pygraph.classes.directed_graph import DirectedGraph
from pygraph.classes.undirected_graph import UndirectedGraph
from pygraph.helpers.functions import convert_graph_directed_to_undirected

def digraph_from_adjacency_list(adjacency_graph):
    digraph = DirectedGraph()
    # Save relations between adjacency list names and node ids 
    name_to_id = {}
    for node in adjacency_graph.keys():
        name_to_id[node] = digraph.new_node()
    for node, adjacent_nodes in adjacency_graph.items():
        for adjacent_node in adjacent_nodes:
            if adjacent_node not in name_to_id.keys():
                name_to_id[adjacent_node] = digraph.new_node()
            digraph.new_edge(name_to_id[node], name_to_id[adjacent_node])
    return digraph, name_to_id

def graph_from_adjacency_list(adjacency_graph):
    digraph, name_to_id = digraph_from_adjacency_list(adjacency_graph)
    return convert_graph_directed_to_undirected(digraph), name_to_id

def graph_to_adjacency_list(digraph):
    adjacency_list = {}

    for node_id in digraph.get_all_node_ids():
        adjacency_list[node_id] = set()
        for neighbor_id in digraph.neighbors(node_id):
            adjacency_list[node_id].add(neighbor_id)

    return adjacency_list

def invert_name_and_id(name_and_id_relation):
 return{v: k for k, v in name_and_id_relation.items()}

def convert_adjacency_list_name_and_id(adjacency_list, name_and_id):
    return {name_and_id[k]:set(
        name_and_id[_v] for _v in v
    ) for k, v in adjacency_list.items()}

def graph_without_nodes_of_edge(graph, edge_id):
    """Returns a copy of this bipartite graph with the given edge and its adjacent nodes removed."""
    new_graph = copy.deepcopy(graph)
    edge_object = new_graph.get_edge(edge_id)
    new_graph.delete_node(edge_object['vertices'][0])
    new_graph.delete_node(edge_object['vertices'][1])
    return new_graph

def graph_without_edge(graph, edge_id):
    """Returns a copy of this bipartite graph with the given edge removed."""
    new_graph = copy.deepcopy(graph)
    new_graph.delete_edge_by_id(edge_id)
    return new_graph

def networkx_graph_without_nodes_of_edge(graph, edge):
    """Returns a copy of this bipartite graph with the given edge and its adjacent nodes removed."""
    new_graph  = graph.copy()
    new_graph.remove_node(edge[0])
    new_graph.remove_node(edge[1])
    return new_graph

def networkx_graph_without_edge(graph, edge):
    """Returns a copy of this bipartite graph with the given edge removed."""
    new_graph  = graph.copy()
    new_graph.remove_edge(*edge)
    return new_graph