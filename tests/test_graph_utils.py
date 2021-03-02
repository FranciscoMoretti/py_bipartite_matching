# -*- coding: utf-8 -*-
import pytest

from py_bipartite_matching.matching.cycle import find_cycle
from py_bipartite_matching.matching.graphs_utils import (
    convert_adjacency_list_name_and_id,
    digraph_from_adjacency_list,
    digraph_from_adjacency_list,
    graph_from_adjacency_list,
    graph_to_adjacency_list,
    invert_name_and_id,
    graph_without_edge,
    graph_without_nodes_of_edge
)

@pytest.mark.parametrize(
    '   graph,                     edge,    expected_graph',
    [
        ({0: {1}},                  [0, 1]                , {}),
        ({0: {1}, 1: {2}},          [0, 1]                , {2: set()}),
        ({0: {1}, 1: {0}},          [0, 1]                , {}),
        ({0: {1}, 1: {0, 2}},       [1, 2]                , {0: set()}),
        ({0: {1, 2}, 1: {0, 2}},    [0, 1]                , {2: set()}),
        ({0: {1, 2}, 1: {0}},       [0, 1]                , {2: set()}),
        ({0: {1}, 1: {2}, 2: {0}},  [0, 1]                , {2: set()}),
        ({0: {2}, 1: {2}},          [0, 2]                , {1: set()}),
        ({0: {2}, 1: {2}, 2: {0}},  [1, 2]                , {0: set()})
    ]
)  # yapf: disable
def test_graph_without_nodes_of_edge(graph, edge, expected_graph):
    digraph, name_to_id = digraph_from_adjacency_list(graph)
    id_to_name = invert_name_and_id(name_to_id)
    edge_id = digraph.get_first_edge_id_by_node_ids(
        name_to_id[edge[0]],
        name_to_id[edge[1]])
    new_digraph = graph_without_nodes_of_edge(digraph, edge_id)
    result_adjacency = graph_to_adjacency_list(new_digraph)
    translated_adjacency = convert_adjacency_list_name_and_id(result_adjacency, id_to_name)
    assert translated_adjacency == expected_graph

@pytest.mark.parametrize(
    '   graph,                     edge,    expected_graph',
    [
        ({0: {1}},                  [0, 1]                , {0:set(), 1: set()}),
        ({0: {1}, 1: {2}},          [0, 1]                , {0:set(), 1: {2}, 2: set()}),
        ({0: {1}, 1: {0}},          [0, 1]                , {0:set(), 1: {0}}),
        ({0: {1}, 1: {0, 2}},       [1, 2]                , {0: {1}, 1: {0}, 2: set()}),
        ({0: {1, 2}, 1: {0, 2}},    [0, 1]                , {0: {2}, 1: {0, 2}, 2: set()}),
        ({0: {1, 2}, 1: {0}},       [0, 1]                , {0: {2}, 1: {0}, 2: set()}),
        ({0: {1}, 1: {2}, 2: {0}},  [0, 1]                , {0: set(), 1: {2}, 2: {0}}),
        ({0: {2}, 1: {2}},          [0, 2]                , {0: set(), 1: {2}, 2: set()}),
        ({0: {2}, 1: {2}, 2: {0}},  [1, 2]                , {0: {2}, 1: set(), 2: {0}})
    ]
)  # yapf: disable
def test_graph_without_edge(graph, edge, expected_graph):
    digraph, name_to_id = digraph_from_adjacency_list(graph)
    id_to_name = invert_name_and_id(name_to_id)
    edge_id = digraph.get_first_edge_id_by_node_ids(
        name_to_id[edge[0]],
        name_to_id[edge[1]])
    new_digraph = graph_without_edge(digraph, edge_id)
    result_adjacency = graph_to_adjacency_list(new_digraph)
    translated_adjacency = convert_adjacency_list_name_and_id(result_adjacency, id_to_name)
    assert translated_adjacency == expected_graph