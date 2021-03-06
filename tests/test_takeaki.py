# -*- coding: utf-8 -*-
import itertools
import math

import hypothesis.strategies as st
from hypothesis import example, given
import pytest

from py_bipartite_matching.matching.bipartite import BipartiteGraph
from py_bipartite_matching.matching.takeaki import enum_perfect_matchings, enum_maximum_matchings


@st.composite
def bipartite_graph(draw):
    m = draw(st.integers(min_value=1, max_value=4))
    n = draw(st.integers(min_value=1, max_value=5))

    graph = BipartiteGraph()
    for i in range(n):
        for j in range(m):
            b = draw(st.booleans())
            if b:
                graph[i, j] = b

    return graph

@given(bipartite_graph())
@example(BipartiteGraph({(0, 2): True, (1, 0): True, (1, 1): True, (2, 0): True, (2, 1): True, (2, 2): True}))
def test_enum_perfect_matchings_correctness(graph):
    size = len(graph._left) # should be equal to graph.right as well
    matchings = set()
    for matching in enum_perfect_matchings(graph):
        assert len(matching) == size, "Matching has a different size than the first one"
        for edge in matching.items():
            assert edge in graph, "Matching contains an edge that was not in the graph"
        frozen_matching = frozenset(matching.items())
        assert frozen_matching not in matchings, "Matching was duplicate"
        matchings.add(frozen_matching)


@given(bipartite_graph())
def test_enum_maximum_matchings_correctness(graph):
    size = None
    matchings = set()
    for matching in enum_maximum_matchings(graph):
        if size is None:
            size = len(matching)
        assert len(matching) == size, "Matching has a different size than the first one"
        for edge in matching.items():
            assert edge in graph, "Matching contains an edge that was not in the graph"
        frozen_matching = frozenset(matching.items())
        assert frozen_matching not in matchings, "Matching was duplicate"
        matchings.add(frozen_matching)


@pytest.mark.parametrize('n, m', filter(lambda x: x[0] >= x[1], itertools.product(range(1, 6), range(0, 4))))
def test_completeness(n, m):
    graph = BipartiteGraph(map(lambda x: (x, True), itertools.product(range(n), range(m))))
    count = sum(1 for _ in enum_maximum_matchings(graph))
    expected_count = m > 0 and math.factorial(n) / math.factorial(n - m) or 0
    assert count == expected_count
