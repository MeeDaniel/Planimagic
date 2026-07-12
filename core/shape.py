"""Base shape support for geometry objects built from key points.

Use ``Shape`` as the common interface for objects such as lines and segments.
It stores a display name, display color, and the points that define the shape.
Concrete subclasses decide what those key points mean geometrically.
"""

from typing import List, Union
from util.definitions import ColorValue
from pygame import Color

from .point import Point


class Shape:
    """Base class for named, colored geometry built from key points.

    Subclasses should pass their defining points to this class and expose any
    extra geometry behavior themselves.
    """

    __next_shape_index = 0
    """Developer note: next numeric suffix for auto-generated shape names."""

    def __init__(
            self,
            key_points: List[Point],
            name: Union[str, None] = None,
            color: Union[ColorValue, None] = None,
        ):
        """Create a shape from its defining points.

        Args:
            key_points: Points that define the shape.
            name: Optional shape name. If omitted, a ``shape_N`` name is used.
            color: Optional display color. Defaults to white.
        """

        self.__name: str
        """Developer note: stable shape name used by ``System`` as a key."""
        self.color: ColorValue
        """Display color used by rendering code that consumes core shapes."""

        if name is None:
            self.__name = "shape_" + str(Shape.__next_shape_index)
            # Increment only after the current index has been used in the name.
            Shape.__next_shape_index += 1
        else:
            self.__name = name

        if color is None:
            self.color = Color("white")
        else:
            self.color = color

        self.__key_points: List[Point] = key_points
        """Developer note: defining point objects, stored in constructor order."""
    
    def get_key_points(self) -> List[Point]:
        """Return a copy of the points that define the shape."""

        # Return a shallow copy so callers cannot reorder the shape's internals.
        return self.__key_points.copy()
    
    def get_name(self) -> str:
        """Return the shape name."""

        return self.__name
