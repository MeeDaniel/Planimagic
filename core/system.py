from typing import Dict

from .point import Point
from .shape import Shape


class System:
    def __init__(self):
        self.__points: Dict[str, Point] = {}
        self.__shapes: Dict[str, Shape] = {}
    
    def add_point(self, point: Point):
        self.__points[point.get_name()] = point
    
    def remove_point(self, name: str):
        point = self.__points.get(name)

        if point is not None:
            del self.__points[name]
    
    def add_shape(self, shape: Shape):
        self.__shapes[shape.get_name()] = shape
    
    def get_points(self) -> Dict[str, Point]:
        return self.__points.copy()

    def get_shapes(self) -> Dict[str, Shape]:
        return self.__shapes.copy()
    
    def clear_system(self):
        self.__points = {}
        self.__shapes = {}
