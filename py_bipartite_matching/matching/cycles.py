# Algorithms to find cycles in a graph 

def find_cycle(graph):
    visited = set()
    for n in graph.get_all_node_ids():
        cycle = _find_cycle(graph, n, [], visited)
        if cycle:
            return cycle
    return []

def _find_cycle(graph, node, path, visited):
    if node in visited:
        try:
            index = path.index(node)
            return path[index:]
        except ValueError:
            return []

    visited.add(node)

    if node not in graph.get_all_node_ids():
        return []

    for other in graph.neighbors(node):
        cycle = _find_cycle(graph, other, path + [node], visited)
        if cycle:
            return cycle

    return []
