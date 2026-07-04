from typing import Tuple, Union
from util.definitions import ColorValue
from pygame.color import Color

from .field import Field
from .general_field import GeneralField


class Point:
    next_name_int: int = 65

    def __init__(
            self,
            x: float,
            y: float,
            name: Union[str, None] = None,
            color: Union[ColorValue, None] = None,
            field: Union[Field, None] = GeneralField()
        ):
        self.__x: float = x
        self.__y: float = y
        self.__name: str
        self.color: ColorValue

        if name is None:
            self.__name = chr(Point.next_name_int)
        else:
            self.__name = name
        
        if color is None:
            self.color = Color("white")
        else:
            self.color = color

        self.field: Union[Field, None] = field
    
    def set_pos(self, x: float, y: float):
        if self.field is not None:
            self.__x, self.__y = self.field.nearest_point(x, y)
    
    def get_pos(self) -> Tuple[float, float]:
        return (self.__x, self.__y)
    
    def get_name(self) -> str:
        return self.__name

    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.__name}(x={self.__x}, y={self.__y})"
