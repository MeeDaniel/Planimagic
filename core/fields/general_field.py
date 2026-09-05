"""Unrestricted field implementation.

Use ``GeneralField`` when points should be allowed to occupy any coordinate.
It satisfies the ``Field`` interface by returning requested coordinates without
modification.
"""

from ..field import Field


class GeneralField(Field):
    """A field that accepts every requested point position."""

    def nearest_point(self, initial_x: float, initial_y: float) -> tuple[float, float]:
        """Return ``(initial_x, initial_y)`` unchanged."""

        return (initial_x, initial_y)
