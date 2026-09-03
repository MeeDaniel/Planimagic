from .line import Line
from .point import Point
from .rule import Rule


class RatioRule(Rule):
    def __init__(
            self,
            name: str,
            line1: Line,
            line2: Line,
            affects: Point
    ):
        super().__init__(name, [line1, line2], [affects])

    def update(self):
        dependencies = self.get_dependencies()

        line1: Line = dependencies[0] # type: ignore
        line2: Line = dependencies[1] # type: ignore

        # TODO: to do
        raise NotImplementedError()

        ax, ay = 0, 0
        affects: Point = self.get_affects()[0] # type: ignore
        affects.set_pos(ax, ay)
