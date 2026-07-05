class UnknownShapeType(TypeError):
    def __init__(self, shape_name: str) -> None:
        super().__init__(
            f"Shape \"{shape_name}\" has unknown derived type. The application does now know how to work with it")