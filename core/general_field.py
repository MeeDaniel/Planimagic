from typing import Tuple

from .field import Field


class GeneralField(Field):
    def nearest_point(self, initial_x: float, initial_y: float) -> Tuple[float, float]:
        return (initial_x, initial_y)