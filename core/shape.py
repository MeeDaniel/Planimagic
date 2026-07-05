from typing import List, Union
from util.definitions import ColorValue
from pygame import Color

from .point import Point


class Shape:
    __next_shape_index = 0

    def __init__(
            self,
            key_points: List[Point],
            name: Union[str, None] = None,
            color: Union[ColorValue, None] = None,
        ):
        self.__name: str
        self.color: ColorValue

        if name is None:
            self.__name = "shape_" + str(Shape.__next_shape_index)
            Shape.__next_shape_index += 1
        else:
            self.__name = name

        if color is None:
            self.color = Color("white")
        else:
            self.color = color

        self.__key_points: List[Point] = key_points
    
    def get_key_points(self) -> List[Point]:
        return self.__key_points.copy()
    
    def get_name(self) -> str:
        return self.__name
