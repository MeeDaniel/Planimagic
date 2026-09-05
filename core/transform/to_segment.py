"""Convert supported shapes into ``Segment`` objects.

Use ``to_segment()`` when code accepts a general ``Shape`` but needs the result
to be represented as a finite ``Segment``. Supported conversions preserve the
original key points and color unless a new name is provided.
"""

from ..shape import Shape
from ..shapes.line import Line
from ..shapes.segment import Segment
from .exceptions import CantTransformFromTo, NotAShape


def to_segment(shape: Shape, new_name: str | None = None) -> Segment:
    """Return ``shape`` represented as a ``Segment``.

    Args:
        shape: Shape instance to convert. ``Segment`` and ``Line`` are
            supported.
        new_name: Optional name for the returned segment. If omitted, the
            original shape name is reused.

    Raises:
        NotAShape: If ``shape`` is not derived from ``Shape``.
        CantTransformFromTo: If the shape is a ``Shape`` subclass that cannot
            currently be converted to ``Segment``.
    """

    if not isinstance(shape, Shape):
        raise NotAShape(shape.__class__)

    if new_name is None:
        # Preserve the existing name by default so transformations are stable.
        new_name = shape.get_name()

    if isinstance(shape, Segment):
        return __from_segment(shape, new_name)

    elif isinstance(shape, Line):
        return __from_line(shape, new_name)
    
    else:
        raise CantTransformFromTo(shape.get_name(), shape.__class__, Segment)

def __from_segment(segment: Segment, new_name: str) -> Segment:
    """Developer note: clone a segment using the requested name.

    The returned object shares the original endpoint objects and color value;
    it does not copy or freeze point coordinates.
    """

    from_, to = segment.get_key_points()
    return Segment(from_, to, new_name, segment.color)

def __from_line(line: Line, new_name: str) -> Segment:
    """Developer note: build a segment from a line's defining points.

    The conversion treats the line's two key points as finite segment
    endpoints.
    """

    from_, to = line.get_key_points()
    return Segment(from_, to, new_name, line.color)
