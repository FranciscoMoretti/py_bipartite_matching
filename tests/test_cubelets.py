# -*- coding: utf-8 -*-
import itertools
import math

import hypothesis.strategies as st
from hypothesis import example, given
import pytest

# from py_bipartite_matching.matching.bipartite import BipartiteGraph, DirectedMatchGraph
# from py_bipartite_matching.matching.takeaki import enum_perfect_matchings, enum_maximum_matchings


# cubelets_matrix = [
#     ["U", "R", "F"],# 0: 0
#     ["D", "F", "R"],# 1: 4
#     ["U", "F", "L"],# 2: 1
#     ["D", "L", "F"],# 3: 5
#     ["U", "L", "B"],# 4: 2
#     ["D", "B", "L"],# 5: 6
#     ["D", "R", "B"],# 6: 7
#     ["U", "B", "R"]]# 7: 3

# example_0 = "FLUUFFLB"

# def create_cubelet_graph(example):
#     edges = []
#     for input_index, element in enumerate(example):
#         for cubelet_index in range(len(cubelets_matrix)):
#             if element in cubelets_matrix[cubelet_index]:
#                 edges.append((input_index, cubelet_index))
#     return BipartiteGraph({e:True for e in edges})       

# # @example(create_cubelet_graph(example_0))
# # @given(bipartite_graph())
# def test_enum_maximum_matchings_correctness():
#     graph = create_cubelet_graph(example_0)
#     size = None
#     matchings = set()
#     for matching in enum_maximum_matchings(graph):
#         if size is None:
#             size = len(matching)
#         assert len(matching) == size, "Matching has a different size than the first one"
#         for edge in matching.items():
#             assert edge in graph, "Matching contains an edge that was not in the graph"
#         frozen_matching = frozenset(matching.items())
#         assert frozen_matching not in matchings, "Matching was duplicate"
#         matchings.add(frozen_matching)


