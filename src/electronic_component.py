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

# All components in 

class Direction(Enum):
  up = "up"
  down = "down"
  left = "left"
  right = "right"

# A component that represents a CircuitJS element
@dataclass
class CircuitJSComponent:
    component_name: str
    anchors: List[str]
    anchors_coords: List[Point]
    value: Optional[float]

@dataclass
class ComponentManifest:
    component: CircuitJSComponent
    shouldFlip: bool
    shouldReverse: bool
    directionMapping: List[Direction]

defaultDirectionMapping: List[Direction] = [Direction.up, Direction.down, Direction.left, Direction.right]

class ElectronicComponent(object):
    
    id: int = 1

    def __init__(self, component_manifest) -> None:
        self.start_coords = component_manifest.start_coords
        self.end_coords: component_manifest.end_coords
        self.value = component_manifest.value
    
    @classmethod
    def anchors(cls, start_terminal, end_terminal):
        return [
            ("start", start_terminal),
            ("end", end_terminal)
        ]

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

    def _direction(self):
        diff_x = self.start_coords.x - self.end_coords.x
        diff_y = self.end_coords.y - self.end_coords.y

        match (diff_x, diff_y):
            case (0, diff_y) if diff_y < 0:
                return Direction.down
            case (0, diff_y) if diff_y > 0:
                return Direction.up
            case (diff_x, 0) if diff_x < 0:
                return Direction.right
            case (diff_x, 0) if diff_x > 0:
                return Direction.left
            case _:
                return Direction.up

    @property
    def shouldReverse(self) -> bool:
        return False  

    @property
    def shouldFlip(self) -> bool:
        return False  


