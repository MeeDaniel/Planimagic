"""Base shape support for geometry objects built from key points.

Use ``Shape`` as the common interface for objects such as lines and segments.
It stores a display name, display color, and the points that define the shape.
Concrete subclasses decide what those key points mean geometrically.
"""

from pygame import Color

from util.definitions import ColorValue

from .point import Point
from .system_unit import SystemUnit


class Shape(SystemUnit):
    """Base class for named, colored geometry built from key points.

    Subclasses should pass their defining points to this class and expose any
    extra geometry behavior themselves.
    """

    def __init__(
            self,
            key_points: list[Point],
            name: str | None = None,
            color: ColorValue | None = None,
            label: str | None = None,
            avoid_system: bool = False
        ):
        """Create a shape from its defining points.

        Args:
            key_points: Points that define the shape.
            name: Optional shape name. If omitted, a ``shape_N`` name is used.
            color: Optional display color. Defaults to white.
            label: Optional point label. If omitted, point name is used.
            avoid_system: Optional checkbox. If on - point will not be added to the system.
        """

        super().__init__(name)

        self.color: ColorValue
        """Display color used by rendering code that consumes core shapes."""
        self.__label: str | None = label
        """Display name. If None, 'name' is used"""

        if color is None:
            self.color = Color("white")
        else:
            self.color = color

        self.__key_points: list[Point] = key_points
        """Developer note: defining point objects, stored in constructor order."""

        if not avoid_system:
            SystemUnit._system.add_shape(self)
    
    def get_key_points(self) -> list[Point]:
        """Return a copy of the points that define the shape."""

        # Return a shallow copy so callers cannot reorder the shape's internals.
        return self.__key_points.copy()

    def get_label(self) -> str:
        if self.__label is None:
            return self.get_name()
        return self.__label

    def set_label(self, label: str | None):
        self.__label = label

    def update(self, *args, **kwargs):
        ...
