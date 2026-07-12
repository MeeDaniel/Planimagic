"""Infinite line shapes defined by two points.

Use ``Line`` when a construction needs a shape that passes through two key
points. The line stores those points through the shared ``Shape`` interface so
rendering or geometry code can treat it like other shapes.
"""

from typing import Union
from util.definitions import ColorValue

from .shape import Shape
from .point import Point


class Line(Shape):
    """A two-point shape representing a line through both points."""

    def __init__(
            self,
            from_: Point,
            to: Point,
            name: Union[str, None] = None,
            color: Union[ColorValue, None] = None
        ):
        """Create a line from two key points.

        Args:
            from_: First point that defines the line.
            to: Second point that defines the line.
            name: Optional shape name. If omitted, ``Shape`` generates one.
            color: Optional display color. Defaults to white.
        """

        # Shape owns common naming, coloring, and key-point storage behavior.
        super().__init__([from_, to], name, color)
