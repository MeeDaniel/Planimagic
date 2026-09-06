"""Infinite line shapes defined by two points.

Use ``Line`` when a construction needs a shape that passes through two key
points. The line stores those points through the shared ``Shape`` interface so
rendering or geometry code can treat it like other shapes.
"""

from util.definitions import ColorValue

from ..point import Point
from ..shape import Shape


class Line(Shape):
    """A two-point shape representing a line through both points."""

    def __init__(
            self,
            from_: Point,
            to: Point,
            name: str | None = None,
            color: ColorValue | None = None,
            label: str | None = None,
            avoid_system: bool = False
        ):
        """Create a line from two key points.

        Args:
            from_: First point that defines the line.
            to: Second point that defines the line.
            name: Optional shape name. If omitted, ``Shape`` generates one.
            color: Optional display color. Defaults to white.
            label: Optional point label. If omitted, point name is used.
            avoid_system: Optional checkbox. If on - point will not be added to the system.
        """

        # Shape owns common naming, coloring, and key-point storage behavior.
        super().__init__([from_, to], name, color, label, avoid_system)

    def dist_to_point_sq(self, point: Point):
        from_, to = self.get_key_points()
        from_x, from_y = from_.get_pos()
        to_x, to_y = to.get_pos()

        __dx = to_x - from_x
        __dy = to_y - from_y
        __len_sq = __dx * __dx + __dy * __dy

        x, y = point.get_pos()
        t = (__dx + __dy) / __len_sq
        return (__dx * t - x) * (__dx * t - x) + (__dy * t - y) * (__dy * t - y)

    def get_point_projection(self, point: Point) -> tuple[float, float]:
        from_, to = self.get_key_points()
        from_x, from_y = from_.get_pos()
        to_x, to_y = to.get_pos()
        p_x, p_y = point.get_pos()

        dx = to_x - from_x
        dy = to_y - from_y
        len_sq = dx * dx + dy * dy

        t = - (dx * from_x + dy * from_y - dx * p_x - dy * p_y) / (len_sq)
        return (
            from_x + dx * t,
            from_y + dy * t
        )

    # def get_dx(self) -> float:
    #     return self.__dx

    # def get_dy(self) -> float:
    #     return self.__dy
    
    # def get_len_sq(self) -> float:
    #     return self.__len_sq
