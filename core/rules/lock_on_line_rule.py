from ..point import Point
from ..rule import Rule
from ..shapes.line import Line


class LockOnLineRule(Rule):
    def __init__(
            self,
            name: str | None,
            point: Point,
            line: Line
    ):
        super().__init__(name, [line], [point])

    def update(self, *args, **kwargs):
        line: Line = self.get_dependencies()[0] # type: ignore
        point: Point = self.get_affects()[0] # type: ignore

        for depending in point.get_incoming():
            if depending is not self:
                self.deactivate()
                return

        ax, ay = line.get_point_projection(point)
        
        point.set_pos(ax, ay)
