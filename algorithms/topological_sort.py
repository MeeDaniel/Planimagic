from collections import defaultdict, deque

from .directed_acyclic_graph import DirectedAcyclicGraph


def topological_sort(_graph: DirectedAcyclicGraph):
    """Kahn's algorithm. Copied from https://youtu.be/NX1_etRg078?si=Scs33-OnID943oXn
    """
    edges = _graph.get_edges()
    # Original algorithm uses `graph` variable. For the high abstract level, `_graph` is related to DirectedAcyclicGraph
    # However, below only `graph` will be used, and will be related only to defaultdict (adjasency matrix).

    graph = defaultdict(list)
    in_degree = defaultdict(int)

    # Build the graph and comute in-degrees
    nodes = set()
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
        nodes.add(u)
        nodes.add(v)

    # Initialize queue with nodes having zero in-degree
    zero_in_degree = deque([node for node in nodes if in_degree[node] == 0])

    topo_order = []

    while zero_in_degree:
        current = zero_in_degree.popleft()
        topo_order.append(current)

        for neighbour in graph[current]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                zero_in_degree.append(neighbour)

    # Check for cycles
    if len(topo_order) != len(nodes):
        raise ValueError("Graph has at least one cycle, topological sort not possible")

    return topo_order
