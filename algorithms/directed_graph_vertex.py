from typing import Any


class DirectedGraphVertex:
    """A vertex of a directed graph.

    The vertex stores an arbitrary value and two protected adjacency lists.
    ``_outgoing`` contains vertices reachable by an outgoing edge from this
    vertex, while ``_incoming`` contains vertices with an edge directed into
    this vertex.

    The adjacency lists are intended to be modified only by a graph class.
    Public callers can inspect them through the copy-returning getter methods.
    """

    value: Any
    #: Value stored in the vertex.
    _outgoing: list["DirectedGraphVertex"]
    #: Vertices connected to this vertex by outgoing edges.
    _incoming: list["DirectedGraphVertex"]
    #: Vertices connected to this vertex by incoming edges.

    def __init__(self, value: Any) -> None:
        """Initialize a vertex with the given value.

        Args:
            value: Arbitrary data associated with the vertex.
        """
        self.value = value
        self._outgoing = []
        self._incoming = []

    def get_outgoing(self) -> list["DirectedGraphVertex"]:
        """Return a shallow copy of the outgoing adjacency list."""
        return self._outgoing.copy()

    def get_incoming(self) -> list["DirectedGraphVertex"]:
        """Return a shallow copy of the incoming adjacency list."""
        return self._incoming.copy()
