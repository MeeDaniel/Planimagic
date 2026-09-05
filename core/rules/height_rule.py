from ..shapes.line import Line
from ..point import Point
from ..rule import Rule


class HeightRule(Rule):
    def __init__(
            self,
            name: str,
            from_point: Point,
            line: Line,
            affects: Point
    ):
        super().__init__(name, [from_point, line], [affects])

    def update(self, *args, **kwargs):
        dependencies = self.get_dependencies()

        from_point: Point = dependencies[0] # type: ignore
        line: Line = dependencies[1] # type: ignore

        ax, ay = line.get_point_projection(from_point)

        affects: Point = self.get_affects()[0] # type: ignore
        affects.set_pos(ax, ay)
