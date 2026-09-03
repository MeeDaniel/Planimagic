from algorithms import DirectedGraphVertex

from .point import Point


class Rule(DirectedGraphVertex):
    __next_rule_index = 65
    """next numeric suffix for auto-generated shape names."""

    def __init__(
            self,
            name: str,
            dependencies: list[DirectedGraphVertex],
            affects: list[Point]
    ):

        super().__init__(value=self) # wdym by value is self???

        self.__name: str
        """Stable rule name used by ``System`` as a key."""
        
        if name is None:
            self.__name = "rule_" + str(Rule.__next_rule_index)
            # Increment only after the current index has been used in the name.
            Rule.__next_rule_index += 1
        else:
            self.__name = name
        
        self.__dependencies = dependencies
        self.__affects = affects

    def update(self) -> None:
        raise NotImplementedError()

    def get_name(self) -> str:
        return self.__name

    def get_dependencies(self) -> list[DirectedGraphVertex]:
        return self.__dependencies

    def get_affects(self) -> list[Point]:
        return self.__affects
