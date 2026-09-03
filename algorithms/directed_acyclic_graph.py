from collections import deque

from .directed_graph_vertex import DirectedGraphVertex


class DirectedAcyclicGraph:
    """A directed graph that does not allow cycles.

    Vertices and edges are maintained as protected collections. Adjacency
    lists belong to the vertices, but they are modified exclusively through
    this graph class so that the edge list and both adjacency directions stay
    consistent.
    """

    _vertices: list[DirectedGraphVertex]
    #: Vertices currently contained in the graph.
    _edges: list[tuple[DirectedGraphVertex, DirectedGraphVertex]]
    #: Directed edges represented as ``(source, target)`` pairs.

    def __init__(self) -> None:
        """Initialize an empty directed acyclic graph."""
        self._vertices = []
        self._edges = []

    def get_vertices(self) -> list[DirectedGraphVertex]:
        """Return a shallow copy of the graph's vertex list."""
        return self._vertices.copy()

    def get_edges(self) -> list[tuple[DirectedGraphVertex, DirectedGraphVertex]]:
        """Return a shallow copy of the graph's edge list."""
        return self._edges.copy()

    def add_vertex(self, vertex: DirectedGraphVertex) -> None:
        """Add a vertex to the graph.

        Args:
            vertex: Vertex to add.

        Raises:
            ValueError: If the vertex is already present in the graph.
        """
        if self._contains_vertex(vertex):
            raise ValueError("The vertex is already present in the graph.")

        self._vertices.append(vertex)

    def remove_vertex(self, vertex: DirectedGraphVertex) -> None:
        """Remove a vertex and all edges incident to it.

        Args:
            vertex: Vertex to remove.

        Raises:
            ValueError: If the vertex is not present in the graph.
        """
        self._require_vertex(vertex)

        incident_edges = [
            edge
            for edge in self._edges
            if edge[0] is vertex or edge[1] is vertex
        ]

        for source, target in incident_edges:
            self.remove_edge(source, target)

        self._vertices.remove(vertex)

    def add_edge(
        self,
        source: DirectedGraphVertex,
        target: DirectedGraphVertex,
    ) -> None:
        """Add a directed edge from ``source`` to ``target``.

        Args:
            source: Vertex from which the edge originates.
            target: Vertex at which the edge ends.

        Raises:
            ValueError: If either vertex is not in the graph, the edge already
                exists, the edge is a self-loop, or the edge would create a
                cycle.
        """
        self._require_vertex(source)
        self._require_vertex(target)

        if source is target:
            raise ValueError("Self-loops are not allowed in a DAG.")

        if self._contains_edge(source, target):
            raise ValueError("The edge already exists in the graph.")

        self.check_certain_cycle(source, target)

        self._edges.append((source, target))
        source._outgoing.append(target)
        target._incoming.append(source)

    def remove_edge(
        self,
        source: DirectedGraphVertex,
        target: DirectedGraphVertex,
    ) -> None:
        """Remove a directed edge from ``source`` to ``target``.

        Args:
            source: Vertex from which the edge originates.
            target: Vertex at which the edge ends.

        Raises:
            ValueError: If the edge does not exist in the graph.
        """
        edge_index = self._find_edge_index(source, target)
        if edge_index == -1:
            raise ValueError("The edge does not exist in the graph.")

        self._edges.pop(edge_index)
        source._outgoing.remove(target)
        target._incoming.remove(source)

    def check_certain_cycle(
        self,
        source: DirectedGraphVertex,
        target: DirectedGraphVertex,
    ) -> None:
        """Raise an error when adding ``source -> target`` would create a cycle.

        The method performs a breadth-first search starting from ``target``.
        If ``source`` is already reachable from ``target``, adding the new
        edge would create a directed cycle.

        The method only checks reachability and does not modify the graph.

        Args:
            source: Proposed source vertex of the new edge.
            target: Proposed target vertex of the new edge.

        Raises:
            ValueError: If either vertex is not in the graph, or if adding the
                proposed edge would create a cycle.
        """
        self._require_vertex(source)
        self._require_vertex(target)

        visited = set()
        queue = deque([target])

        while queue:
            current = queue.popleft()

            if current is source:
                raise ValueError("The edge would create a cycle.")

            vertex_id = id(current)
            if vertex_id in visited:
                continue

            visited.add(vertex_id)
            queue.extend(current._outgoing)

    def _contains_vertex(self, vertex: DirectedGraphVertex) -> bool:
        """Return whether the exact vertex object belongs to the graph."""
        return any(current is vertex for current in self._vertices)

    def _require_vertex(self, vertex: DirectedGraphVertex) -> None:
        """Raise an error when the exact vertex object is not in the graph."""
        if not self._contains_vertex(vertex):
            raise ValueError("The vertex is not present in the graph.")

    def _contains_edge(
        self,
        source: DirectedGraphVertex,
        target: DirectedGraphVertex,
    ) -> bool:
        """Return whether the exact directed edge is present in the graph."""
        return self._find_edge_index(source, target) != -1

    def _find_edge_index(
        self,
        source: DirectedGraphVertex,
        target: DirectedGraphVertex,
    ) -> int:
        """Return an edge's index, or ``-1`` when the edge is absent."""
        for index, (current_source, current_target) in enumerate(self._edges):
            if current_source is source and current_target is target:
                return index

        return -1
