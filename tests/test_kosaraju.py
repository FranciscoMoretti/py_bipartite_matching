# -*- coding: utf-8 -*-
import itertools
import math

import hypothesis.strategies as st
from hypothesis import example, given
import pytest

from py_bipartite_matching.matching.kosaraju import Kosaraju
from py_bipartite_matching.matching.bipartite import BipartiteGraph
# @example(create_cubelet_graph(example_0))
# @given(bipartite_graph())
def test_kosaraju():
    # Create a graph given in the above diagram 
    g = Kosaraju(5)
    g.addEdge(1, 2) 
    g.addEdge(0, 1) 
    g.addEdge(2, 3) 
    g.addEdge(3, 0) 
    g.addEdge(3, 2) 
    g.addEdge(3, 4) 
    scc = g.getSCC() 
    assert scc == {frozenset({4}), frozenset({0, 1, 2, 3})}
