from util.definitions import ColorValue

from ..point import Point
from ..shape import Shape


class Ray(Shape):
    def __init__(
            self,
            base: Point,
            direction_point: Point,
            name: str | None = None,
            color: ColorValue | None = None,
            label: str | None = None,
            avoid_system: bool = False
        ):super().__init__([base, direction_point], name, color, label, avoid_system)
    
    def get_pos_by_proportion(self, proportion: float) -> tuple[float, float]:
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

    def get_base_point(self) -> Point:
        base, _ = self.get_key_points()
        return base

    def get_direction_point(self) -> Point:
        _, direction = self.get_key_points()
        return direction
