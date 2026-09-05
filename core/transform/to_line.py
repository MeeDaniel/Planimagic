"""Convert supported shapes into ``Line`` objects.

Use ``to_line()`` when code accepts a general ``Shape`` but needs the result to
be represented as a ``Line``. Supported conversions preserve the original key
points and color unless a new name is provided.
"""

from ..shape import Shape
from ..shapes.line import Line
from ..shapes.segment import Segment
from .exceptions import CantTransformFromTo, NotAShape


def to_line(shape: Shape, new_name: str | None = None) -> Line:
    """Return ``shape`` represented as a ``Line``.

    Args:
        shape: Shape instance to convert. ``Line`` and ``Segment`` are
            supported.
        new_name: Optional name for the returned line. If omitted, the original
            shape name is reused.

    Raises:
        NotAShape: If ``shape`` is not derived from ``Shape``.
        CantTransformFromTo: If the shape is a ``Shape`` subclass that cannot
            currently be converted to ``Line``.
    """

    if not isinstance(shape, Shape):
        raise NotAShape(shape.__class__)

    if new_name is None:
        # Preserve the existing name by default so transformations are stable.
        new_name = shape.get_name()

    if isinstance(shape, Line):
        return __from_line(shape, new_name)

    elif isinstance(shape, Segment):
        return __from_segment(shape, new_name)
    
    else:
        raise CantTransformFromTo(shape.get_name(), shape.__class__, Line)

def __from_line(line: Line, new_name: str) -> Line:
    """Developer note: clone a line using the requested name.

    The returned object shares the original key point objects and color value;
    it does not copy or freeze point coordinates.
    """

    from_, to = line.get_key_points()
    return Line(from_, to, new_name, line.color)

def __from_segment(segment: Segment, new_name: str) -> Line:
    """Developer note: build a line through a segment's endpoints.

    The conversion treats segment endpoints as the two defining points of the
    resulting infinite line.
    """

    from_, to = segment.get_key_points()
    return Line(from_, to, new_name, segment.color)
