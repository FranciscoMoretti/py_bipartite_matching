# -*- coding: utf-8 -*-
import networkx as nx

from py_bipartite_matching.py_bipartite_matching import enum_perfect_matchings
from py_bipartite_matching.graphs_utils import top_nodes, bottom_nodes


def print_debug_info(graph, matchings):
    print("Graph and matchings")
    print(f"Nodes :{graph.nodes}")
    print(f"Edges :{graph.edges}")
    print("Matchings :")
    for number, matching in enumerate(matchings):
        print(f"{number}: {set(matching)}")
    print("-" * 80)


cubelets_matrix = [
    ["U", "R", "F"],  # 0: 0
    ["D", "F", "R"],  # 1: 4
    ["U", "F", "L"],  # 2: 1
    ["D", "L", "F"],  # 3: 5
    ["U", "L", "B"],  # 4: 2
    ["D", "B", "L"],  # 5: 6
    ["D", "R", "B"],  # 6: 7
    ["U", "B", "R"]
]  # 7: 3

example_0 = "FLUUFFLB"


def create_cubelet_graph(example):
    graph = nx.Graph()

    for count, value in enumerate(example):
        graph.add_node(count, bipartite=0, label=value)
    for count, value in enumerate(cubelets_matrix, start=len(example)):
        graph.add_node(count, bipartite=1, label=value)

    for top_node in top_nodes(graph):
        for bottom_node in bottom_nodes(graph):
            if graph.nodes[top_node]['label'] in graph.nodes[bottom_node]['label']:
                graph.add_edge(top_node, bottom_node)

    return graph


def test_cubelets_enum_perfect_matchings():
    print("Testing cubelets_enum_perfect_matchings")

    graph = create_cubelet_graph(example_0)

    if len(list(top_nodes(graph))) != len(list(bottom_nodes(graph))):
        pass

    size = len(list(top_nodes(graph)))  # should be equal to graph.right as well
    matchings = set()
    for matching in enum_perfect_matchings(graph):
        assert len(matching) == size, "Matching has a different size than the first one"
        for edge in matching.items():
            assert edge in graph.edges, "Matching contains an edge that was not in the graph"
        frozen_matching = frozenset(matching.items())
        assert frozen_matching not in matchings, "Matching was duplicate"
        matchings.add(frozen_matching)
    print_debug_info(graph=graph, matchings=matchings)
