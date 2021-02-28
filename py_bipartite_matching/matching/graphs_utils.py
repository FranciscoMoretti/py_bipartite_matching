# utils for graphs of the PyGraph library 
from pygraph.classes.directed_graph import DirectedGraph

def digraph_from_adjacency_list(adjacency_graph):
    digraph = DirectedGraph()
    # Save relations between adjacency list names and node ids 
    name_to_id = {}
    for node, adjacent_nodes in adjacency_graph.items():
        if node not in name_to_id.keys():
            name_to_id[node] = digraph.new_node()
        for adjacent_node in adjacent_nodes:
            if adjacent_node not in name_to_id.keys():
                name_to_id[adjacent_node] = digraph.new_node()
            digraph.new_edge(name_to_id[node], name_to_id[adjacent_node])
    return digraph, name_to_id

def invert_name_and_id(name_and_id_relation):
 return{v: k for k, v in name_and_id_relation.items()}