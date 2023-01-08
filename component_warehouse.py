



from electronic_component import ElectronicComponent


class ComponentWarehouse:
    def __init__(self) -> None:
        self.classes: dict[str, ElectronicComponent] = {}

    def add_class(self, c: ElectronicComponent) -> None:
        self.classes[c.name] = c

    def component(self, c: ElectronicComponent) -> ElectronicComponent:
        self.add_class(c)
        return c 

    def __getitem__(self, n: str) -> ElectronicComponent:
        return self.classes[n]

component_warehouse = ComponentWarehouse()
