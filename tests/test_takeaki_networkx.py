# -*- coding: utf-8 -*-
import itertools
import math

import hypothesis.strategies as st
from hypothesis import example, given
import pytest

from py_bipartite_matching.matching.bipartite import BipartiteGraph
from py_bipartite_matching.matching.takeaki_networkx import enum_perfect_matchings_networkx, enum_maximum_matchings_networkx, create_directed_matching_graph

from py_bipartite_matching.matching.networkx_biparite_sample import davis_southern_women_graph
from networkx.algorithms.bipartite.matching import maximum_matching
import networkx as nx

@st.composite
def bipartite_graph(draw):
    m = draw(st.integers(min_value=1, max_value=4))
    n = draw(st.integers(min_value=1, max_value=5))
    top_nodes = list(range(m))
    bottom_nodes = list(range(10, 10+n))

    graph = nx.Graph()
    graph.add_nodes_from(top_nodes, bipartite=0)
    graph.graph["top"] = top_nodes
    graph.add_nodes_from(bottom_nodes, bipartite=1)
    graph.graph["bottom"] = bottom_nodes
    for i in top_nodes:
        for j in bottom_nodes:
            if draw(st.booleans()):
                graph.add_edge(i, j)

    return graph

@given(bipartite_graph())
@example(BipartiteGraph({(0, 2): True, (1, 0): True, (1, 1): True, (2, 0): True, (2, 1): True, (2, 2): True}))
def test_enum_perfect_matchings_correctness_networkx(graph):
    graph =  davis_southern_women_graph()
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
def test_enum_maximum_matchings_correctness_networkx(graph):
    size = None
    matchings = set()
    for matching in enum_maximum_matchings_networkx(graph):
        if size is None:
            size = len(matching)
        assert len(matching) == size, "Matching has a different size than the first one"
        for edge in matching.items():
            assert graph.has_edge(*edge), "Matching contains an edge that was not in the graph"
        frozen_matching = frozenset(matching.items())
        assert frozen_matching not in matchings, "Matching was duplicate"
        matchings.add(frozen_matching)

@pytest.mark.parametrize('n', range(1, 6))
def test_perfect_matchings_completeness_networkx(n):
    top_nodes = list(range(n))
    bottom_nodes = list(range(10, 10+n))
    edges = itertools.product(top_nodes, bottom_nodes)
    # create the graph
    graph = nx.Graph()
    graph.add_nodes_from(top_nodes, bipartite=0)
    graph.graph["top"] = top_nodes
    graph.add_nodes_from(bottom_nodes, bipartite=1)
    graph.graph["bottom"] = bottom_nodes
    graph.add_edges_from(edges)

    count = sum(1 for _ in enum_perfect_matchings_networkx(graph))
    expected_count = int(math.factorial(n))
    assert count == expected_count

@pytest.mark.parametrize('n, m', filter(lambda x: x[0] >= x[1], itertools.product(range(1, 6), range(0, 4))))
def test_maximum_matchings_completeness_networkx(n, m):
    top_nodes = list(range(n))
    bottom_nodes = list(range(10, 10+m))
    edges = itertools.product(top_nodes, bottom_nodes)
    # create the graph
    graph = nx.Graph()
    graph.add_nodes_from(top_nodes, bipartite=0)
    graph.graph["top"] = top_nodes
    graph.add_nodes_from(bottom_nodes, bipartite=1)
    graph.graph["bottom"] = bottom_nodes
    graph.add_edges_from(edges)

    count = sum(1 for _ in enum_maximum_matchings_networkx(graph))
    expected_count = m > 0 and int(math.factorial(n) / math.factorial(n - m)) or 0
    assert count == expected_count


def test_create_directed_matching_graph():
    graph =  davis_southern_women_graph()
    matching = maximum_matching(G=graph, top_nodes=graph.graph['top'])
    digraph = create_directed_matching_graph(graph=graph, top_nodes=graph.graph['top'], matching=matching)
    assert graph.nodes == digraph.nodes
    assert len(graph.edges) == len(digraph.edges)