

from abc import ABC, abstractmethod
from schemdraw import Drawing
from electronic_component import ElectronicComponent

class Visitor(ABC):
    @abstractmethod
    def visit_any(self, d: Drawing, element: ElectronicComponent) -> None:
        pass

    @abstractmethod
    def visit_three_terminal(self, d: Drawing, element: ElectronicComponent) -> None:
        pass


