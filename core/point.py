"""Named points constrained by a geometry field.

Use this module when you need a point object with a display name, a color, and
coordinates. A point can be moved with ``set_pos()``, read with ``get_pos()``,
and identified with ``get_name()``.
"""

from pygame.color import Color

from util.definitions import ColorValue

from .system_unit import SystemUnit


class Point(SystemUnit):
    """A named coordinate pair.

    ``Point`` is the basic geometric object used by shapes and systems.
    """

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            name: str | None = None,
            color: ColorValue | None = None,
            label: str | None = None,
            avoid_system: bool = False
        ):
        """Create a point at ``(x, y)``.

        Args:
            x: Requested x-coordinate.
            y: Requested y-coordinate.
            name: Optional point name. If omitted, a generated name is used.
            color: Optional display color. Defaults to white.
            label: Optional point label. If omitted, point name is used.
            avoid_system: Optional checkbox. If on - point will not be added to the system.
        """

        super().__init__(name)

        self.__x: float = x
        """Developer note: stored x-coordinate after field adjustment."""
        self.__y: float = y
        """Developer note: stored y-coordinate after field adjustment."""
        self.color: ColorValue
        """Display color used by rendering code that consumes core points."""
        self.__label: str | None = label
        """Display name. If None, 'name' is used"""
        
        if color is None:
            self.color = Color("white")
        else:
            self.color = color

        if not avoid_system:
            SystemUnit._system.add_point(self)
    
    def set_pos(self, x: float, y: float):
        """Move the point to the nearest field-approved position.

        Args:
            x: Requested x-coordinate.
            y: Requested y-coordinate.
        """

        self.__x, self.__y = x, y
    
    def get_pos(self) -> tuple[float, float]:
        """Return the current ``(x, y)`` coordinates."""

        return (self.__x, self.__y)

    def get_label(self) -> str:
        if self.__label is None:
            return self.get_name()
        return self.__label

    def set_label(self, label: str | None):
        self.__label = label

    def update(self, *args, **kwargs):
        ...

    def __str__(self) -> str:
        """Return the readable representation used by ``str(point)``."""

        return self.__repr__()
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation of the point."""

        return f"{self.__class__.__name__}.{self.get_name()}(x={self.__x}, y={self.__y})"
