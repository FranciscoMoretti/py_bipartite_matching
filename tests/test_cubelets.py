# -*- coding: utf-8 -*-
import networkx as nx

from py_bipartite_matching.py_bipartite_matching import enum_perfect_matchings


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
    # Create helper functions
    def ind_to_btm(ind):
        return ind + 10

    def btm_to_ind(ind):
        return ind - 10

    graph = nx.Graph()
    size = len(example)

    top_nodes = list(range(size))
    bottom_nodes = list(range(ind_to_btm(0), ind_to_btm(size)))

    graph.add_nodes_from(top_nodes, bipartite=0)
    graph.graph["top"] = top_nodes
    graph.add_nodes_from(bottom_nodes, bipartite=1)
    graph.graph["bottom"] = bottom_nodes

    for top_node, element in enumerate(example):
        for bottom_node in bottom_nodes:
            if element in cubelets_matrix[btm_to_ind(bottom_node)]:
                graph.add_edge(top_node, bottom_node)

    return graph


def test_cubelets_enum_perfect_matchings():
    print("Testing cubelets_enum_perfect_matchings")

    graph = create_cubelet_graph(example_0)

    if len(graph.graph['top']) != len(graph.graph['bottom']):
        pass

    size = len(graph.graph['top'])  # should be equal to graph.right as well
    matchings = set()
    for matching in enum_perfect_matchings(graph):
        assert len(matching) == size, "Matching has a different size than the first one"
        for edge in matching.items():
            assert edge in graph.edges, "Matching contains an edge that was not in the graph"
        frozen_matching = frozenset(matching.items())
        assert frozen_matching not in matchings, "Matching was duplicate"
        matchings.add(frozen_matching)
    print_debug_info(graph=graph, matchings=matchings)
