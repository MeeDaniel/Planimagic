from typing import List

from .point import Point


class Shape:
    def __init__(self):
        self.__key_points: List[Point] = [
            Point(0, 0),
            Point(1, 0),
            Point(0, 1),
            Point(1, 1)
        ]
    
    def get_key_points(self) -> List[Point]:
        return self.__key_points.copy()
