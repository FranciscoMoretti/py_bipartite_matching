#!/usr/bin/env python
"""Tests for `py_bipartite_matching` package."""
# -*- coding: utf-8 -*-
import itertools
import math

import hypothesis.strategies as st
from hypothesis import given, example
import pytest

from py_bipartite_matching.brute_force_bipartite_matching import (
    brute_force_enum_perfect_matchings, brute_force_enum_maximum_matchings)
from py_bipartite_matching.py_bipartite_matching import enum_perfect_matchings, enum_maximum_matchings
import py_bipartite_matching.graphs_utils as gu

from networkx.algorithms.bipartite.matching import maximum_matching
import networkx as nx

# Known limitation of pylint to process composites from hypothesis
# pylint: disable=no-value-for-parameter; `draw` provided by `@composite`


def print_debug_info(graph, matchings):
    print("Graph and matchings")
    print(f"Nodes :{graph.nodes}")
    print(f"Edges :{graph.edges}")
    print("Matchings :")
    for number, matching in enumerate(matchings):
        print(f"{number}: {set(matching)}")
    print("-" * 80)


@st.composite
def bipartite_graph_inputs(draw):
    # Slect the number of nodes on each side of the biparite  graph
    n = draw(st.integers(min_value=1, max_value=5))
    m = draw(st.integers(min_value=1, max_value=5))
    # Create a random bipartite graph with k edges
    k = draw(st.integers(min_value=0, max_value=n * m))
    # Select some seeds to have randomness but also reproducibility
    seed = draw(st.integers(min_value=0, max_value=3))
    return (n, m, k, seed)


@st.composite
def balanced_bipartite_graph_inputs(draw):
    # For a perfect matching to exist the bipartite graph must have the same
    # the same number of vertex on each partition
    n = draw(st.integers(min_value=1, max_value=5))
    # Create a random bipartite graph with k edges
    k = draw(st.integers(min_value=0, max_value=n * n))
    # Select some seeds to have randomness but also reproducibility
    seed = draw(st.integers(min_value=0, max_value=3))
    return (n, k, seed)


@given(balanced_bipartite_graph_inputs())
def test_enum_perfect_matchings_correctness(n_k_seed):
    print("Testing enum_perfect_matchings_correctness")
    n, k, seed = n_k_seed
    graph = nx.bipartite.gnmk_random_graph(n, n, k, seed)

    if len(list(gu.top_nodes(graph))) != len(list(gu.bottom_nodes(graph))):
        pass

    size = len(list(gu.top_nodes(graph)))  # should be equal to graph.right as well
    matchings = set()
    for matching in enum_perfect_matchings(graph):
        assert len(matching) == size, "Matching has a different size than the first one"
        for edge in matching.items():
            assert edge in graph.edges, "Matching contains an edge that was not in the graph"
        frozen_matching = frozenset(matching.items())
        assert frozen_matching not in matchings, "Matching was duplicate"
        matchings.add(frozen_matching)
    brute_matchings = {frozenset(matching.items()) for matching in \
        brute_force_enum_perfect_matchings(graph)}
    assert matchings == brute_matchings
    print_debug_info(graph=graph, matchings=matchings)


@given(bipartite_graph_inputs())
@example((5, 3, 7, 0))
def test_enum_maximum_matchings_correctness(n_m_k_seed):
    print("Testing enum_maximum_matchings_correctness")
    n, m, k, seed = n_m_k_seed
    graph = nx.bipartite.gnmk_random_graph(n, m, k, seed)

    size = None
    matchings = set()
    for matching in enum_maximum_matchings(graph):
        if size is None:
            size = len(matching)
        assert len(matching) == size, "Matching has a different size than the first one"
        for edge in matching.items():
            assert graph.has_edge(*edge), "Matching contains an edge that was not in the graph"
        frozen_matching = frozenset(matching.items())
        assert frozen_matching not in matchings, "Matching was duplicate"
        matchings.add(frozen_matching)
    print_debug_info(graph=graph, matchings=matchings)


@pytest.mark.parametrize('n', range(1, 6))
def test_perfect_matchings_completeness(n):
    print("Testing perfect_matchings_completeness")
    # Create a complete bipartite graph
    graph = nx.complete_bipartite_graph(n, n, nx.Graph)
    # Create a set of matchings to be sure there are no repetitions
    matchings = {frozenset(matching.items()) for matching in \
        enum_perfect_matchings(graph)}
    brute_force_matchings = {frozenset(matching.items()) for matching in \
        brute_force_enum_perfect_matchings(graph)}
    assert matchings == brute_force_matchings
    # The matchings count should be equal to n!
    assert len(matchings) == int(math.factorial(n))
    print_debug_info(graph=graph, matchings=matchings)


@pytest.mark.parametrize('n, m', itertools.product(range(1, 6), range(0, 4)))
def test_maximum_matchings_completeness(n, m):
    print("Testing maximum_matchings_completeness")
    # Create a complete bipartite graph
    graph = nx.complete_bipartite_graph(n, m, nx.Graph)
    # Create a set of matchings to be sure there are no repetitions
    matchings = {frozenset(matching.items()) for matching in \
        enum_maximum_matchings(graph)}
    # The matchings count should be equal to n!/(n-m)! if m > 0, 0 otherwise
    expected_count = int(math.factorial(max(n, m)) / math.factorial(abs(n - m))) if m > 0 else 0
    assert len(matchings) == expected_count
    print_debug_info(graph=graph, matchings=matchings)


@given(bipartite_graph_inputs())
def test_create_directed_matching_graph(n_m_k_seed):
    n, m, k, seed = n_m_k_seed
    graph = nx.bipartite.gnmk_random_graph(n, m, k, seed)

    matching = maximum_matching(G=graph, top_nodes=gu.top_nodes(graph))
    digraph = gu.create_directed_matching_graph(graph=graph,
                                                top_nodes=gu.top_nodes(graph),
                                                matching=matching)
    assert graph.nodes == digraph.nodes
    assert len(graph.edges) == len(digraph.edges)


@given(balanced_bipartite_graph_inputs())
def test_brute_force_enum_perfect_matchings(n_k_seed):
    print("Testing brute_force_enum_perfect_matchings_correctness")
    n, k, seed = n_k_seed
    graph = nx.bipartite.gnmk_random_graph(n, n, k, seed)

    matchings = {frozenset(matching.items()) for matching in \
        enum_perfect_matchings(graph)}
    brute_force_matchings = {frozenset(matching.items()) for matching in \
        brute_force_enum_perfect_matchings(graph)}
    assert matchings == brute_force_matchings
    print_debug_info(graph=graph, matchings=matchings)


@given(bipartite_graph_inputs())
def test_brute_force_enum_maximum_matchings(n_m_k_seed):
    print("Testing brute_force_enum_maximum_matchings")
    n, m, k, seed = n_m_k_seed
    graph = nx.bipartite.gnmk_random_graph(n, m, k, seed)

    matchings = {frozenset(matching.items()) for matching in \
        enum_maximum_matchings(graph)}
    brute_force_matchings = {frozenset(matching.items()) for matching in \
        brute_force_enum_maximum_matchings(graph)}
    assert matchings == brute_force_matchings
    print_debug_info(graph=graph, matchings=matchings)
