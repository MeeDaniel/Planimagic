from ..point import Point
from ..rule import Rule
from ..shapes.line import Line


class HeightRule(Rule):
    def __init__(
            self,
            name: str | None,
            from_point: Point,
            line: Line,
            affects: Point,
            avoid_system: bool = False
    ):
        super().__init__(name, [from_point, line], [affects], avoid_system)

    def update(self, *args, **kwargs):
        dependencies = self.get_dependencies()

        from_point: Point = dependencies[0] # type: ignore
        line: Line = dependencies[1] # type: ignore

        ax, ay = line.get_point_projection(from_point)

        affects: Point = self.get_affects()[0] # type: ignore
        affects.set_pos(ax, ay)
