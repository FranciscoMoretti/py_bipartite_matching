from typing import Dict, List

from py_bipartite_matching.matching.hopcroft_karp import HopcroftKarp
import networkx as nx 


class TestHopcroftKarp:
    """
    Testing the implementation of the Hopcroft Karp algorithm.
    """

    def test_hopcroft_karp(self):

        graph: Dict[int, List[str]] = {
            0: ["v0", "v1"],
            1: ["v0", "v4"],
            2: ["v2", "v3"],
            3: ["v0", "v4"],
            4: ["v0", "v3"],
        }
        expected: Dict[int, str] = {0: "v1", 1: "v4", 2: "v2", 3: "v0", 4: "v3"}
        hk = HopcroftKarp[int, str](graph)
        matchings, maximum_matching = hk.get_maximum_matching_num()
        assert maximum_matching == expected
        assert matchings == 5

        graph: Dict[str, List[int]] = {'A': [1, 2], 'B': [2, 3], 'C': [2], 'D': [3, 4, 5, 6],
                                       'E': [4, 7], 'F': [7], 'G': [7]}
        expected: Dict[str, int] = {'A': 1, 'B': 3, 'C': 2, 'D': 5, 'E': 4, 'F': 7}
        hk = HopcroftKarp[str, int](graph)
        matchings, maximum_matching = hk.get_maximum_matching_num()
        assert maximum_matching == expected
        assert matchings == 6

        graph: Dict[int, List[str]] = {1: ['a', 'c'], 2: ['a', 'c'], 3: ['c', 'b'], 4: ['e']}
        expected: Dict[int, str] = {1: 'a', 2: 'c', 3: 'b', 4: 'e'}
        hk = HopcroftKarp[int, str](graph)
        matchings, maximum_matching = hk.get_maximum_matching_num()
        assert maximum_matching == expected
        assert matchings == 4

        graph: Dict[str, List[int]] = {'A': [3, 4], 'B': [3, 4], 'C': [3], 'D': [1, 5, 7],
                                       'E': [1, 2, 7], 'F': [2, 8], 'G': [6], 'H': [2, 4, 8]}
        expected: Dict[str, int] = {'A': 3, 'B': 4, 'D': 1, 'E': 7, 'F': 8, 'G': 6, 'H': 2}
        hk = HopcroftKarp[str, int](graph)
        matchings, maximum_matching = hk.get_maximum_matching_num()
        assert maximum_matching == expected
        assert matchings == 7


class TestHopcroftKarpNetworkx:
    """
    Testing the implementation of the Hopcroft Karp algorithm.
    """
    def test_hopcroft_karp(self):

        G = nx.Graph()
        G.add_edge(0, "v0")
        G.add_edge(0, "v1")
        G.add_edge(1, "v0")
        G.add_edge(1, "v4")
        G.add_edge(2, "v2")
        G.add_edge(2, "v3")
        G.add_edge(3, "v0")
        G.add_edge(3, "v4")
        G.add_edge(4, "v0")
        G.add_edge(4, "v3")

        matching = nx.bipartite.hopcroft_karp_matching(G)
        matching = {k: v for (k, v) in matching.items() if isinstance(k, int)}
        expected: Dict[int, str] = {0: "v1", 1: "v4", 2: "v2", 3: "v0", 4: "v3"}

        assert matching == expected
        assert len(matching) == 5

        G = nx.Graph()
        G.add_edge('A', 1)
        G.add_edge('A', 2)
        G.add_edge('B', 2)
        G.add_edge('B', 3)
        G.add_edge('C', 2)
        G.add_edge('D', 3)
        G.add_edge('D', 4)
        G.add_edge('D', 5)
        G.add_edge('D', 6)
        G.add_edge('E', 4)
        G.add_edge('E', 7)
        G.add_edge('F', 7)
        G.add_edge('G', 7)

        expected1: Dict[str, int] = {'A': 1, 'B': 3, 'C': 2, 'D': 5, 'E': 4, 'F': 7}
        expected2: Dict[str, int] = {'A': 1, 'B': 3, 'C': 2, 'D': 5, 'E': 4, 'G': 7}
        matching = nx.bipartite.hopcroft_karp_matching(G)
        matching = {k: v for (k, v) in matching.items() if isinstance(k, str)}
        assert matching == expected1 or matching == expected2
        assert len(matching) == 6

        G = nx.Graph()
        G.add_edge(1, "a")
        G.add_edge(1, "c")
        G.add_edge(2, "a")
        G.add_edge(2, "c")
        G.add_edge(3, "c")
        G.add_edge(3, "b")
        G.add_edge(4, "e")

        expected: Dict[int, str] = {1: 'a', 2: 'c', 3: 'b', 4: 'e'}
        matching = nx.bipartite.hopcroft_karp_matching(G, {1, 2, 3, 4})
        matching = {k: v for (k, v) in matching.items() if isinstance(k, int)}
        assert matching == expected
        assert len(matching) == 4

        G = nx.Graph()
        # G.add_edge('A', 3)
        G.add_edge('A', 4)
        # G.add_edge('B', 3)
        G.add_edge('B', 4)
        G.add_edge('C', 3)
        G.add_edge('D', 1)
        G.add_edge('D', 5)
        G.add_edge('D', 7)
        # G.add_edge('E', 1)
        G.add_edge('E', 2)
        G.add_edge('E', 7)
        # G.add_edge('F', 2)
        G.add_edge('F', 8)
        G.add_edge('G', 6)
        G.add_edge('H', 2)
        G.add_edge('H', 4)
        G.add_edge('H', 8)

        expected1: Dict[str, int] = {'A': 4,'C': 3, 'D': 1, 'E': 7, 'F': 8, 'G': 6, 'H': 2}
        expected2: Dict[str, int] = {'B': 4,'C': 3, 'D': 1, 'E': 7, 'F': 8, 'G': 6, 'H': 2}
        matching = nx.bipartite.hopcroft_karp_matching(G, {'A','B','C','D','E','F','G','H'})
        matching = {k: v for (k, v) in matching.items() if isinstance(k, str)}
        assert matching == expected1 or matching == expected2
        assert len(matching) == 7
