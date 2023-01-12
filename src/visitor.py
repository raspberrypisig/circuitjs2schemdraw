

from abc import ABC, abstractmethod
from schemdraw import Drawing
from .electronic_component import ElectronicComponent

class Visitor(ABC):
    @abstractmethod
    def visit_any(self, d: Drawing, element: ElectronicComponent) -> None:
        pass

    #@abstractmethod
    #def visit_three_terminal(self, d: Drawing, element: ElectronicComponent) -> None:
    #    pass

class SchemDrawVisitor(Visitor):    
    def visit_any(self, component):        
        print(component)
        element = component.schemdraw_element
        #args = component.schemdraw_args
        #label_value = component.label_value
        #label_id = component.label_id
        print(element)
        '''
        d.push()
        element_args = {}
        element_args['d'] = element.direction
        if element.shouldReverse:
            element_args["reverse"] = True
        c = element.getElement()(**element_args)
        d += c
        here = d.here
        d.pop()
        '''


