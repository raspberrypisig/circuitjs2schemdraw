



from electronic_component import ElectronicComponent


class ComponentWarehouse:
    def __init__(self) -> None:
        self.classes: dict[str, ElectronicComponent] = {}

    def add_class(self, c: ElectronicComponent) -> None:
        self.classes[c.name] = c

    # -- the decorator
    def component(self, c: ElectronicComponent) -> ElectronicComponent:
        self.add_class(c)

        # Decorators have to return the function/class passed (or a modified variant thereof), however I'd rather do this separately than retroactively change add_class, so.
        # "held" is more succint, anyway.
        return c 

    def __getitem__(self, n: str) -> ElectronicComponent:
        return self.classes[n]

component_warehouse = ComponentWarehouse()
