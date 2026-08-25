class Camera:
    def __init__(self, x: float, y: float, scale: float):
        """TODO: Write a proper docstring

        Args:
            x (float): X-coordinate of a camera
            y (float): Y-coordinate of a camera
            scale (float): size of one system unit in pixels
        """

        self.x = x
        self.y = y
        self.scale = scale

    def unit2display(
            self,
            object_x: float,
            object_y: float,
            window_width: float,
            window_height: float
    ) -> tuple[float, float]:
        return (
            (object_x - self.x) * self.scale + window_width / 2,
            (object_y - self.y) * self.scale + window_height / 2
        )

    def display2unit(
            self,
            object_x: float,
            object_y: float,
            window_width: float,
            window_height: float
    ) -> tuple[float, float]:
        return (
            (object_x - window_width / 2) / self.scale + self.x,
            (object_y - window_height / 2) / self.scale + self.y,
        )
    