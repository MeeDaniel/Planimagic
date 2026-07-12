"""Finite line segments defined by two endpoints.

Use ``Segment`` when a construction needs the bounded part between two points.
The segment exposes its endpoints through ``Shape.get_key_points()`` and can
interpolate positions along the segment with ``get_pos_by_proportion()``.
"""

from typing import Union, Tuple
from util.definitions import ColorValue

from .shape import Shape
from .point import Point


class Segment(Shape):
    """A two-point shape representing the finite segment between endpoints."""

    def __init__(
            self,
            from_: Point,
            to: Point,
            name: Union[str, None] = None,
            color: Union[ColorValue, None] = None
        ):
        """Create a segment from two endpoint points.

        Args:
            from_: Segment start point.
            to: Segment end point.
            name: Optional shape name. If omitted, ``Shape`` generates one.
            color: Optional display color. Defaults to white.
        """

        # Shape owns common naming, coloring, and endpoint storage behavior.
        super().__init__([from_, to], name, color)
    
    def get_pos_by_proportion(self, proportion: float) -> Tuple[float, float]:
        """Return a point along the segment.

        Args:
            proportion: Linear position between the endpoints. ``0`` returns
                the start point, ``1`` returns the end point, and values outside
                that range extrapolate beyond the segment.
        """

        from_, to = self.get_key_points()
        from_x, from_y = from_.get_pos()
        to_x, to_y = to.get_pos()
        # Linear interpolation is performed independently for each axis.
        return (
            from_x + (to_x - from_x) * proportion,
            from_y + (to_y - from_y) * proportion
        )
