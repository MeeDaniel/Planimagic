"""Named points constrained by a geometry field.

Use this module when you need a point object with a display name, a color, and
coordinates that are validated by a ``Field``. A point can be moved with
``set_pos()``, read with ``get_pos()``, and identified with ``get_name()``.
"""

from pygame.color import Color

from algorithms import DirectedGraphVertex
from util.definitions import ColorValue

from .field import Field
from .general_field import GeneralField


class Point(DirectedGraphVertex):
    """A named coordinate pair that belongs to an optional field.

    ``Point`` is the basic geometric object used by shapes and systems. Its
    stored coordinates are adjusted through its field, so callers can attach a
    custom ``Field`` to constrain where the point may be placed.
    """

    __next_name_int: int = 65
    """Developer note: ASCII code used for generated point names.

    The current implementation reads this value when ``name`` is omitted. It is
    kept private because generated-name policy is an implementation detail of
    ``Point`` rather than part of the public API.
    """

    def __init__(
            self,
            x: float,
            y: float,
            name: str | None = None,
            color: ColorValue | None = None,
            field: Field | None = GeneralField()
        ):
        """Create a point at ``(x, y)``.

        Args:
            x: Requested x-coordinate.
            y: Requested y-coordinate.
            name: Optional point name. If omitted, a generated name is used.
            color: Optional display color. Defaults to white.
            field: Optional field that constrains the stored position. Defaults
                to ``GeneralField``, which accepts every coordinate.
        """

        super().__init__(value=self) # wdym by value is self???

        self.__x: float = x
        """Developer note: stored x-coordinate after field adjustment."""
        self.__y: float = y
        """Developer note: stored y-coordinate after field adjustment."""
        self.__name: str
        """Developer note: point name used by ``System`` as the dictionary key."""
        self.color: ColorValue
        """Display color used by rendering code that consumes core points."""

        if name is None:
            # ASCII 65 is "A", which is the first generated point label.
            self.__name = chr(Point.__next_name_int)
        else:
            self.__name = name
        
        if color is None:
            self.color = Color("white")
        else:
            self.color = color

        self.field: Field | None = field
        """Field that projects requested coordinates onto allowed positions."""

        self.set_pos(*self.get_pos())  # Re-apply the initial coordinates through the field.
    
    def set_pos(self, x: float, y: float):
        """Move the point to the nearest field-approved position.

        Args:
            x: Requested x-coordinate.
            y: Requested y-coordinate.
        """

        if self.field is not None:
            self.__x, self.__y = self.field.nearest_point(x, y)
    
    def get_pos(self) -> tuple[float, float]:
        """Return the current ``(x, y)`` coordinates."""

        return (self.__x, self.__y)
    
    def get_name(self) -> str:
        """Return the point name."""

        return self.__name

    def __str__(self) -> str:
        """Return the readable representation used by ``str(point)``."""

        return self.__repr__()
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation of the point."""

        return f"{self.__class__.__name__}.{self.__name}(x={self.__x}, y={self.__y})"
