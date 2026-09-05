from algorithms import DirectedGraphVertex


class SystemUnit(DirectedGraphVertex):
    __next_id: int = 0

    __class_is_inited: bool = False
    __taken_names: set[str]

    @staticmethod
    def __init_class():
        SystemUnit.__taken_names = set()
        SystemUnit.__class_is_inited = True
    
    def __init__(self, name: str | None = None):
        if not SystemUnit.__class_is_inited:
            SystemUnit.__init_class()

        super().__init__(self)
        self.__name: str

        if name is None:
            name = "uu_" + str(SystemUnit.__next_id) # Unnamed unit <?>
            SystemUnit.__next_id += 1

        if name in SystemUnit.__taken_names:
            raise ValueError("Such unit name is already taken.")

        self.__name = name
        SystemUnit.__taken_names.add(name)

        self.__is_active: bool = True

    def get_name(self) -> str:
        return self.__name

    def is_active(self) -> bool:
        return self.__is_active

    def activate(self):
        self.__is_active = True

    def deactivate(self):
        self.__is_active = False

    def update(self, *args, **kwargs):
        raise NotImplementedError()

    def gain_inactivity(self):
        for su in self.get_incoming():
            if isinstance(su, SystemUnit) and not su.is_active():
                self.__is_active = False
                break
