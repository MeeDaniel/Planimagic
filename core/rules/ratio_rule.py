from ..point import Point
from ..rule import Rule
from ..shapes.segment import Segment


class RatioRule(Rule):
    def __init__(
            self,
            name: str,
            segment: Segment,
            ratio: float,
            affects: Point
    ):
        super().__init__(name, [segment], [affects])
        self.ratio = ratio

    def update(self, *args, **kwargs):
        segment: Segment = self.get_dependencies()[0] # type: ignore

        from_, to = segment.get_key_points()
        fx, fy = from_.get_pos()
        tx, ty = to.get_pos()
        ax = fx + (tx - fx) * self.ratio
        ay = fy + (ty - fy) * self.ratio

        affects: Point = self.get_affects()[0] # type: ignore
        affects.set_pos(ax, ay)
