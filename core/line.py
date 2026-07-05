from typing import Union
from util.definitions import ColorValue

from .shape import Shape
from .point import Point


class Line(Shape):
    def __init__(
            self,
            from_: Point,
            to: Point,
            name: Union[str, None] = None,
            color: Union[ColorValue, None] = None
        ):
        super().__init__([from_, to], name, color)
