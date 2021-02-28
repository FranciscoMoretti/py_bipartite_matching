# utils for graphs of the PyGraph library 
import copy
from pygraph.classes.directed_graph import DirectedGraph
from pygraph.classes.undirected_graph import UndirectedGraph

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

 
def convert_graph_directed_to_undirected(dg):
    """Converts a directed graph into an undirected graph. Directed edges are made undirected."""

    udg = UndirectedGraph()

    # Copy the graph
    # --Copy nodes
    # --Copy edges
    udg.nodes = copy.deepcopy(dg.nodes)
    udg.edges = copy.deepcopy(dg.edges)
    udg.next_node_id = dg.next_node_id
    udg.next_edge_id = dg.next_edge_id
    udg.num_nodes = dg.num_nodes

    # Convert the directed edges into undirected edges
    for edge_id in udg.get_all_edge_ids():
        edge = udg.get_edge(edge_id)
        target_node_id = edge['vertices'][1]
        target_node = udg.get_node(target_node_id)
        target_node['edges'].append(edge_id)
        udg.num_edges = len(udg.get_all_edge_ids())

    return udg