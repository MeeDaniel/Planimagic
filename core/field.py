"""Coordinate constraint interface for points.

Use ``Field`` as the base class for objects that decide where a ``Point`` is
allowed to be placed. A field receives a requested coordinate and returns the
nearest coordinate that belongs to the allowed area.
"""

from typing import Tuple


class Field:
    """Base interface for point placement constraints.

    Subclasses implement ``nearest_point()`` to map any requested coordinate to
    the closest coordinate they allow.
    """

    def nearest_point(self, initial_x: float, initial_y: float) -> Tuple[float, float]:
        """Return the allowed coordinate nearest to ``(initial_x, initial_y)``.

        Args:
            initial_x: Requested x-coordinate.
            initial_y: Requested y-coordinate.

        Raises:
            NotImplementedError: Always raised by the base class. Use a
                concrete subclass such as ``GeneralField``.
        """

        raise NotImplementedError()
