# -*- coding: utf-8 -*-
import pytest

from py_bipartite_matching.matching.bipartite import BipartiteGraph, DirectedMatchGraph


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
def test_directed_graph_find_cycle(graph, expected_cycle):
    dmg = DirectedMatchGraph({}, {})
    dmg.update(graph)
    cycle = dmg.find_cycle()
    if len(expected_cycle) > 0:
        assert expected_cycle[0] in cycle
        start = cycle.index(expected_cycle[0])
        cycle = cycle[start:] + cycle[:start]
    assert cycle == expected_cycle


class TestBipartiteGraphTest:
    def test_setitem(self):
        graph = BipartiteGraph()

        graph[0, 1] = True

        with pytest.raises(TypeError):
            graph[0] = True

        with pytest.raises(TypeError):
            graph[0, ] = True

        with pytest.raises(TypeError):
            graph[0, 1, 2] = True

    def test_getitem(self):
        graph = BipartiteGraph({(0, 0): True})

        assert graph[0, 0] == True

        with pytest.raises(TypeError):
            _ = graph[0]

        with pytest.raises(TypeError):
            _ = graph[0, ]

        with pytest.raises(TypeError):
            _ = graph[0, 1, 2]

        with pytest.raises(KeyError):
            _ = graph[0, 1]

    def test_delitem(self):
        graph = BipartiteGraph({(0, 0): True})

        assert (0, 0) in graph

        del graph[0, 0]

        assert (0, 0) not in graph

        with pytest.raises(TypeError):
            del graph[0]

        with pytest.raises(TypeError):
            del graph[0, ]

        with pytest.raises(TypeError):
            del graph[0, 1, 2]

        with pytest.raises(KeyError):
            del graph[0, 1]

    def test_limited_to(self):
        graph = BipartiteGraph({(0, 0): True, (1, 0): True, (1, 1): True, (0, 1): True})

        assert graph.limited_to({0}, {0}) == {(0, 0): True}
        assert graph.limited_to({0, 1}, {1}) == {(0, 1): True, (1, 1): True}
        assert graph.limited_to({1}, {1}) == {(1, 1): True}
        assert graph.limited_to({1}, {0, 1}) == {(1, 0): True, (1, 1): True}
        assert graph.limited_to({0, 1}, {0, 1}) == graph

    def test_eq(self):
        assert BipartiteGraph() == {}
        assert {} == BipartiteGraph()
        assert BipartiteGraph({(1, 1): True}) == {(1, 1): True}
        assert {(1, 1): True} == BipartiteGraph({(1, 1): True})
        assert not BipartiteGraph({(1, 2): True}) == {(1, 1): True}
        assert not {(1, 2): True} == BipartiteGraph({(1, 1): True})
        assert not BipartiteGraph() == ''
        assert not '' == BipartiteGraph()
