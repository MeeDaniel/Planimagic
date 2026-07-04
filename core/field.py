from typing import Tuple


# Determines where point may exist. If user wants to move the point, it selects the new spot. This spot goes through this
# class as "initial" spot. The function finds the closest point in the allowed area and place the point in 
class Field:
    def nearest_point(self, initial_x: float, initial_y: float) -> Tuple[float, float]:
        raise NotImplementedError()
