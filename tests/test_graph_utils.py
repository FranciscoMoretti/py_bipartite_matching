# -*- coding: utf-8 -*-
import pytest

import networkx as nx
from py_bipartite_matching.graphs_utils import graph_without_edge, graph_without_nodes_of_edge

@pytest.mark.parametrize(
    '   adjacency_list,             edge,               expected_adjacency_list',
    [
        ({0: {1}},                  [0, 1]              , {}),
        ({0: {1}, 1: {2}},          [0, 1]              , {2: set()}),
        ({0: {1}, 1: {0}},          [0, 1]              , {}),
        ({0: {1}, 1: {0, 2}},       [1, 2]              , {0: set()}),
        ({0: {1, 2}, 1: {0, 2}},    [0, 1]              , {2: set()}),
        ({0: {1, 2}, 1: {0}},       [0, 1]              , {2: set()}),
        ({0: {1}, 1: {2}, 2: {0}},  [0, 1]              , {2: set()}),
        ({0: {2}, 1: {2}},          [0, 2]              , {1: set()}),
        ({0: {2}, 1: {2}, 2: {0}},  [1, 2]              , {0: set()})
    ]
)  # yapf: disable
def test_graph_without_nodes_of_edge(adjacency_list, edge, expected_adjacency_list):
    graph = nx.Graph(adjacency_list)
    new_graph = graph_without_nodes_of_edge(graph, edge)
    expected_graph = nx.Graph(expected_adjacency_list)
    assert nx.is_isomorphic(new_graph, expected_graph)

@pytest.mark.parametrize(
    '   adjacency_list,             edge,    expected_adjacency_list',
    [
        ({0: {1}},                  [0, 1]                , {0: set(), 1: set()}),
        ({0: {1}, 1: {2}},          [0, 1]                , {0: set(), 1: {2}, 2: {1}}),
        ({0: {1}, 1: {0}},          [0, 1]                , {0: set(), 1: set()}),
        ({0: {1}, 1: {0, 2}},       [1, 2]                , {0: {1}, 1: {0}, 2: set()}),
        ({0: {1, 2}, 1: {0, 2}},    [0, 1]                , {0: {2}, 1: {2}, 2: {0, 1}}),
        ({0: {1, 2}, 1: {0}},       [0, 1]                , {0: {2}, 1: set(), 2: {0}}),
        ({0: {1}, 1: {2}, 2: {0}},  [0, 1]                , {0: {2}, 1: {2}, 2: {0, 1}}),
        ({0: {2}, 1: {2}},          [0, 2]                , {0: set(), 1: {2}, 2: {1}}),
        ({0: {2}, 1: {2}, 2: {0}},  [1, 2]                , {0: {2}, 1: set(), 2: {0}})
    ]
)  # yapf: disable
def test_graph_without_edge(adjacency_list, edge, expected_adjacency_list):
    graph = nx.Graph(adjacency_list)
    new_graph = graph_without_edge(graph, edge)
    expected_graph = nx.Graph(expected_adjacency_list)
    assert nx.is_isomorphic(new_graph, expected_graph)
