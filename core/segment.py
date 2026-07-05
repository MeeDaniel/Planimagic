from typing import Union, Tuple
from util.definitions import ColorValue

from .shape import Shape
from .point import Point


class Segment(Shape):
    def __init__(
            self,
            from_: Point,
            to: Point,
            name: Union[str, None] = None,
            color: Union[ColorValue, None] = None
        ):
        super().__init__([from_, to], name, color)
    
    def get_pos_by_proportion(self, proportion: float) -> Tuple[float, float]:
        from_, to = self.get_key_points()
        from_x, from_y = from_.get_pos()
        to_x, to_y = to.get_pos()
        return (
            from_x + (to_x - from_x) * proportion,
            from_y + (to_y - from_y) * proportion
        )
