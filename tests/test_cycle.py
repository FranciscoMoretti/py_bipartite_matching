# -*- coding: utf-8 -*-
import pytest

from py_bipartite_matching.matching.cycle import find_cycle
from py_bipartite_matching.matching.graphs_utils import digraph_from_adjacency_list, graph_from_adjacency_list, invert_name_and_id

@pytest.mark.parametrize(
    '   graph,                      expected_cycle',
    [
        ({},                        []),
        ({0: {1}},                  []),
        ({0: {1}, 1: {2}},          []),
        ({0: {1}, 1: {0}},          [0, 1]),
        ({0: {1}, 1: {0}},          [1, 0]),
        ({0: {1}, 1: {0, 2}},       [0, 1]),
        ({0: {1, 2}, 1: {0, 2}},    [0, 1]),
        ({0: {1, 2}, 1: {0}},       [0, 1]),
        ({0: {1}, 1: {2}, 2: {0}},  [0, 1, 2]),
        ({0: {2}, 1: {2}},          []),
        ({0: {2}, 1: {2}, 2: {0}},  [0, 2]),
        ({0: {2}, 1: {2}, 2: {1}},  [1, 2]),
    ]
)  # yapf: disable
def test_pygraph_digraph_find_cycle(graph, expected_cycle):
    digraph, name_to_id = digraph_from_adjacency_list(graph)
    id_to_name = invert_name_and_id(name_to_id)
    cycle_ids = find_cycle(digraph)
    cycle_names = [id_to_name[id] for id in cycle_ids]
    if len(expected_cycle) > 0:
        assert expected_cycle[0] in cycle_names
        start = cycle_names.index(expected_cycle[0])
        cycle_names = cycle_names[start:] + cycle_names[:start]
    assert cycle_names == expected_cycle



@pytest.mark.parametrize(
    '   graph,                             expected_cycle',
    [
        ({},                               []),
        ({0: {1}},                         []),
        ({0: {1}, 1: {2}},                 []),
        ({0: {1}, 1: {0}},                 []),
        ({0: {1}, 1: {0}},                 []),
        ({0: {1}, 1: {0, 2}},              []),
        ({0: {1, 2}, 1: {0, 2}},           [0, 1, 2]),
        ({0: {1, 2}, 1: {0}},              []),
        ({0: {1, 2}, 1: {2}},              [0, 1, 2]),
        ({0: {1}, 1: {2}, 2: {0}},         [0, 1, 2]),
        ({0: {1}, 1: {2}, 2: {3}, 3:{0}},  [0, 1, 2, 3]),
        ({0: {2}, 1: {2}},                 []),
        ({0: {2}, 1: {2}, 2: {0}},         []),
        ({0: {2}, 1: {2}, 2: {1}},         []),
    ]
)  # yapf: disable
def test_pygraph_graph_find_cycle(graph, expected_cycle):
    digraph, name_to_id = graph_from_adjacency_list(graph)
    id_to_name = invert_name_and_id(name_to_id)
    cycle_ids = find_cycle(digraph, directed=False)
    cycle_names = [id_to_name[id] for id in cycle_ids]
    if len(expected_cycle) > 0:
        assert expected_cycle[0] in cycle_names
        start = cycle_names.index(expected_cycle[0])
        cycle_names = cycle_names[start:] + cycle_names[:start]
    assert cycle_names == expected_cycle
