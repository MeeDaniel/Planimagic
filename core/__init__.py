"""Core geometry model for GeometrySmart.

This package contains the application-independent domain objects used to
describe a geometric workspace:

- ``Point`` stores a named coordinate constrained by a ``Field``.
- ``Field`` defines where points are allowed to exist, while ``GeneralField``
  accepts every coordinate unchanged.
- ``Shape`` is the base object for geometry built from key points.
- ``Line`` and ``Segment`` are concrete two-point shapes.
- ``System`` is the in-memory collection of points and shapes that represents
  the current construction.

The imports below form the package's public API, allowing callers to use
``from core import Point, Segment, System`` instead of importing each module
directly.
"""

from .point import Point  # noqa: F401
from .rule import Rule  # noqa: F401
from .rules import *
from .shape import Shape  # noqa: F401
from .shapes import *
from .system import System  # noqa: F401
from .system_unit import SystemUnit  # noqa: F401
