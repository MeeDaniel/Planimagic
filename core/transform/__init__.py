"""Shape transformation helpers for the core geometry model.

Use this package when a shape needs to be converted into another compatible
shape type while preserving its key points, color, and optionally its name.
The public helpers currently support conversion between ``Line`` and
``Segment``.
"""

from .exceptions import CantTransformFromTo, NotAShape, UnknownShapeType  # noqa: F401
from .to_line import to_line  # noqa: F401
from .to_segment import to_segment  # noqa: F401
