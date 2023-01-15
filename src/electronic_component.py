#
# Base class for components
#

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional
from schemdraw import Drawing
#from .visitor import Visitor
from .point import Point
from .schemdraw_manifest import SchemdrawElementManifest


# A component that represents a CircuitJS element
@dataclass
class CircuitJSComponent:
    component_name: str
    anchors: List[str]
    anchors_coords: List[Point]
    value: Optional[float]

#@dataclass
#class ComponentManifest:
#    component: CircuitJSComponent
#    shouldFlip: bool
#    shouldReverse: bool

class ElectronicComponent(object):    
    id: int = 1

    def __init__(self, component_manifest) -> None:
        self.start_coords = component_manifest.start_coords
        self.end_coords = component_manifest.end_coords
        self.value = component_manifest.value
        
    
    @property
    def has_length(self):
        return True

    @property
    def label_value(self):
        return self.value

    #@property
    #def label_id(self):
    #    return self.id

    @classmethod
    def anchors(cls, start_terminal, end_terminal):
        return [
            ("start", start_terminal),
            ("end", end_terminal)
        ]

    @property
    def end_anchors(self):
        return ["end"]

    @property
    def other_anchors(self):
        return [
            {"end": Point(0.0, 0.0)}
        ]
            
    def get_end_coord(self):
        if self.start_coords < self.end_coords:
          return self.end_coords
        else:
          return self.start_coords

    def get_start_coord(self):
        if self.start_coords < self.end_coords:
          return self.start_coords
        else:
          return self.end_coords    

    def convert_coordinates(self, anchor, start_anchor_pos):
        pass

    @property
    def name(self) -> str:
        return self.__name__

    @property
    def hasValue(self) -> bool:
        return True

    @property
    def hasLabel(self) -> bool:
        return True

    # TODO: replace this 
    #@property
    #def sorted_endpoints(self):
    #    terminal_coords = [self._start_coords, self._end_coords]
    #    sorted_coordinates = sorted(terminal_coords, key=lambda x: (x[0], int(x[1])))
    #    return sorted_coordinates


    @property
    def shouldReverse(self) -> bool:
        return False  

    @property
    def shouldFlip(self) -> bool:
        return False  


