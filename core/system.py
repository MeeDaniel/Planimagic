"""In-memory collection for points and shapes.

Use ``System`` as the container for the current geometric construction. It
stores points and shapes by name, supports adding and removing objects, and can
return snapshots of the registered objects for rendering or inspection.
"""

from typing import Dict

from .point import Point
from .shape import Shape


class System:
    """A named registry of points and shapes in a construction."""

    def __init__(self):
        """Create an empty system."""

        self.__points: Dict[str, Point] = {}
        """Developer note: point registry keyed by ``Point.get_name()``."""
        self.__shapes: Dict[str, Shape] = {}
        """Developer note: shape registry keyed by ``Shape.get_name()``."""
    
    def add_point(self, point: Point):
        """Add or replace a point by its name.

        Args:
            point: Point to register in the system.
        """

        self.__points[point.get_name()] = point
    
    def remove_point(self, name: str):
        """Remove a point by name if it exists.

        Args:
            name: Name of the point to remove.
        """

        point = self.__points.get(name)

        if point is not None:
            # Deletion is guarded so missing names are ignored rather than raised.
            del self.__points[name]
    
    def add_shape(self, shape: Shape):
        """Add or replace a shape by its name.

        Args:
            shape: Shape to register in the system.
        """

        self.__shapes[shape.get_name()] = shape
    
    def get_points(self) -> Dict[str, Point]:
        """Return a copy of the registered points dictionary."""

        # Return a shallow copy so callers cannot replace the registry itself.
        return self.__points.copy()

    def get_shapes(self) -> Dict[str, Shape]:
        """Return a copy of the registered shapes dictionary."""

        # Return a shallow copy so callers cannot replace the registry itself.
        return self.__shapes.copy()
    
    def clear_system(self):
        """Remove all points and shapes from the system."""

        self.__points = {}
        self.__shapes = {}
