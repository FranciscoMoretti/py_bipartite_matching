# -*- coding: utf-8 -*-
"""
Contains classes and functions to enumerate matchings based on brute force methods.
"""
from typing import Iterator, Any, Dict

import itertools
import networkx as nx
from networkx.algorithms.bipartite.matching import maximum_matching

from .graphs_utils import (top_nodes, bottom_nodes)

__all__ = ['brute_force_enum_perfect_matchings']


def brute_force_enum_perfect_matchings(graph: nx.Graph) -> Iterator[Dict[Any, Any]]:
    if len(list(top_nodes(graph))) != len(list(bottom_nodes(graph))):
        return
    size = len(list(top_nodes(graph)))
    matching = maximum_matching(graph, top_nodes=top_nodes(graph))
    matching = {k: v for k, v in matching.items() if k in top_nodes(graph)}
    if matching and len(matching) == size:
        for values in itertools.product(
                *map(lambda node: graph.neighbors(node), top_nodes(graph))):
            if len(set(values)) == len(values):
                matching = {k: v for k, v in zip(top_nodes(graph), values)}
                yield matching


def brute_force_enum_maximum_matchings(graph: nx.Graph) -> Iterator[Dict[Any, Any]]:
    matching = maximum_matching(graph, top_nodes=top_nodes(graph))
    matching = {k: v for k, v in matching.items() if k in top_nodes(graph)}
    matching_len = len(matching)
    if matching_len == 0:
        return
    for edges in itertools.combinations(graph.edges(), matching_len):
        if len({edge[0] for edge in edges}) < matching_len:
            continue
        if len({edge[1] for edge in edges}) < matching_len:
            continue
        yield dict(edges)
