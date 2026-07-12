"""Exceptions raised by core shape transformation helpers.

Use these exception types to distinguish invalid transformation requests from
other geometry errors. They are raised by ``to_line()`` and ``to_segment()``
when input is not a shape or when a shape type has no supported conversion.
"""

class UnknownShapeType(TypeError):
    """Raised when a shape name refers to an unsupported derived shape type."""

    def __init__(self, shape_name: str) -> None:
        """Create an error for an unknown shape type.

        Args:
            shape_name: Name of the shape whose concrete type is unknown.
        """

        super().__init__(
            f"Shape \"{shape_name}\" has unknown derived type. The application does now know how to work with it"
        )

class NotAShape(TypeError):
    """Raised when a transformation receives an object that is not a ``Shape``."""

    def __init__(self, class_) -> None:
        """Create an error for a non-shape input class.

        Args:
            class_: Class of the invalid object passed to a transformation.
        """

        super().__init__(
            f"{str(class_)} is not derived from class \"Shape\""
        )

class CantTransformFromTo(TypeError):
    """Raised when a shape cannot be converted to the requested shape type."""

    def __init__(self, shape_name: str, from_class, to_class):
        """Create an error for an unsupported shape conversion.

        Args:
            shape_name: Name of the shape being converted.
            from_class: Current concrete class of the shape.
            to_class: Target shape class requested by the caller.
        """

        super().__init__(
            f"Shape \"{shape_name}\" of type {str(from_class)} cannot be transformed to shape of type {str(to_class)}"
        )
