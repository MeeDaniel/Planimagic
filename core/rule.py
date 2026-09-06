from .point import Point
from .system_unit import SystemUnit


class Rule(SystemUnit):
    def __init__(
            self,
            name: str | None,
            dependencies: list[SystemUnit],
            affects: list[Point],
            avoid_system: bool = False
    ):

        super().__init__(name)
        
        self.__dependencies = dependencies
        self.__affects = affects

        if not avoid_system:
            SystemUnit._system.add_rule(self)
    
    def get_dependencies(self) -> list[SystemUnit]:
        return self.__dependencies

    def get_affects(self) -> list[Point]:
        return self.__affects
