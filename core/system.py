"""In-memory collection for points and shapes.

Use ``System`` as the container for the current geometric construction. It
stores points and shapes by name, supports adding and removing objects, and can
return snapshots of the registered objects for rendering or inspection.
"""

from algorithms import DirectedAcyclicGraph, topological_sort

from .point import Point
from .rule import Rule
from .shape import Shape


class System(DirectedAcyclicGraph):
    """A named registry of points and shapes in a construction."""

    def __init__(self):
        """Create an empty system."""

        super().__init__()

        self.__points: dict[str, Point] = {}
        """Developer note: point registry keyed by ``Point.get_name()``."""
        self.__shapes: dict[str, Shape] = {}
        """Developer note: shape registry keyed by ``Shape.get_name()``."""
        self.__rules: dict[str, Rule] = {}
        """Rule registry keyed by ``Rule.get_name()``."""
        self.__topo_order: list[Rule] = []
        """The order in which rules should be updated"""

    def add_point(self, point: Point):
        """Add or replace a point by its name.

        Args:
            point: Point to register in the system.
        """

        self.__points[point.get_name()] = point
        self.add_vertex(point)
        self.__update_topo()

    def remove_point(self, name: str):
        """Remove a point by name if it exists.

        Args:
            name: Name of the point to remove.
        """

        point = self.__points.get(name)

        if point is not None:
            # Deletion is guarded so missing names are ignored rather than raised.
            del self.__points[name]
            self.remove_vertex(point)
            self.__update_topo()

    def add_shape(self, shape: Shape):
        """Add or replace a shape by its name.

        Args:
            shape: Shape to register in the system.
        """

        self.__shapes[shape.get_name()] = shape

        self.add_vertex(shape)
        for key_point in shape.get_key_points():
            self.add_edge(key_point, shape)

        self.__update_topo()

    def remove_shape(self, name: str):
        """Remove a shape by name if it exists

        Args:
            name (str): Name of the shape to remove
        """

        shape = self.__shapes.get(name)

        if shape is not None:
            del self.__shapes[name]
            self.remove_vertex(shape)
            self.__update_topo()

    def add_rule(self, rule: Rule):
        """Add or replace a rule by its name.

        Args:
            rule (Rule): Rule to register in the system
        """

        self.__rules[rule.get_name()] = rule

        self.add_vertex(rule)
        for dependency in rule.get_dependencies():
            self.add_edge(dependency, rule)
        for affects in rule.get_affects():
            self.add_edge(rule, affects)

        self.__update_topo()

    def remove_rule(self, name: str):
        """Remove a rule by name if it exists

        Args:
            name (str): Name of the rule to remove
        """

        rule = self.__rules.get(name)

        if rule is not None:
            del self.__rules[name]
            self.remove_vertex(rule)
            self.__update_topo()

    def get_points(self) -> dict[str, Point]:
        """Return a copy of the registered points dictionary."""

        # Return a shallow copy so callers cannot replace the registry itself.
        return self.__points.copy()

    def get_shapes(self) -> dict[str, Shape]:
        """Return a copy of the registered shapes dictionary."""

        # Return a shallow copy so callers cannot replace the registry itself.
        return self.__shapes.copy()

    def get_rules(self) -> dict[str, Rule]:
        """Return a copy of the registered rules dictionary."""

        # Return a shallow copy so callers cannot replace the registry itself.
        return self.__rules.copy()
    
    def clear_system(self):
        """Remove all points and shapes from the system."""

        self.__points = {}
        self.__shapes = {}

        for v in self.get_vertices():
            self.remove_vertex(v)

        self.__update_topo()

    def update_rules(self):
        for rule in self.__topo_order:
            rule.update()

    def __update_topo(self):
        self.__topo_order.clear()
        order = topological_sort(self)
        for v in order:
            if isinstance(v, Rule):
                self.__topo_order.append(v)
