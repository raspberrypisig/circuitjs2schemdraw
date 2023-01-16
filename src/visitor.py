

from abc import ABC, abstractmethod
from schemdraw import Drawing
from .electronic_component import ElectronicComponent
from .schemdraw_manifest import SchemdrawElementManifest
from .component_warehouse import component_warehouse

class Visitor(ABC):
    @abstractmethod
    def visit_any(self, d: Drawing, element: ElectronicComponent) -> None:
        pass

    #@abstractmethod
    #def visit_three_terminal(self, d: Drawing, element: ElectronicComponent) -> None:
    #    pass

class SchemDrawVisitor(Visitor):    
    def visit_any(self, component):        
        #print(component)
        element_class = component.schemdraw_element   
        args = component.schemdraw_args
        other_anchors = component.other_anchors
        start_coord = component.get_start_coord()
        end_coord = component.get_end_coord()
        has_length = component.has_length
        #print(end_coord)
        label_value = component.label_value
        return [SchemdrawElementManifest(element_class, 
        args, 
        other_anchors, 
        start_coord, 
        end_coord, 
        has_length)]

    def visit_three_terminal(self, component) -> None:
        wire_length, wire_end = component.anchor_coords
        direction = component._direction()
        wire_start = component.start_coords
        component.start_coords = wire_end
        three_terminal_component = self.visit_any(component)
        wire = component_warehouse['wire'].fromargs(component.start_coords, wire_end)
        
        wire_element_class = wire.schemdraw_element   
        wire_args = {"d": direction}
        wire_other_anchors = wire.other_anchors
        wire_start_coord = wire_start
        wire_end_coord = wire.get_end_coord()
        wire_has_length = wire.has_length        

        wire_manifest = SchemdrawElementManifest(wire_element_class, 
        wire_args, 
        wire_other_anchors, 
        wire_start_coord, 
        wire_end_coord, 
        wire_has_length
        )
        return [wire_manifest] + three_terminal_component


