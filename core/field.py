from typing import Tuple


class Field:
    def nearest_point(self, initial_x: float, initial_y: float) -> Tuple[float, float]:
        raise NotImplementedError()
