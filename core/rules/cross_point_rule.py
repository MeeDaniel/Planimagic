from ..point import Point
from ..rule import Rule
from ..shapes.line import Line


class CrossPointRule(Rule):
    def __init__(
            self,
            name: str | None,
            line1: Line,
            line2: Line,
            affects: Point
    ):
        super().__init__(name, [line1, line2], [affects])

    def update(self, *args, **kwargs):
        dependencies = self.get_dependencies()

        line1: Line = dependencies[0] # type: ignore
        line2: Line = dependencies[1] # type: ignore
        A, B = line1.get_key_points()
        C, D = line2.get_key_points()
        x1, y1 = A.get_pos()
        x2, y2 = B.get_pos()
        x3, y3 = C.get_pos()
        x4, y4 = D.get_pos()

        t = ((x3 - x1) * (y4 - y3) + (x4 - x3) * (y1 - y3)) / ((x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1))
        ax = x1 + (x2 - x1) * t
        ay = y1 + (y2 - y1) * t

        affects: Point = self.get_affects()[0] # type: ignore
        affects.set_pos(ax, ay)
