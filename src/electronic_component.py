#
# Base class for components
#

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from schemdraw import Drawing
from .visitor import Visitor
from .point import Point

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

    def __init__(self, component_name: str, start_coord: Point, end_coord: Point, value: Optional[float] = None) -> None:
        self._component_name: str = component_name
        self._start_coord: Point = start_coord
        self._end_coord: Point = end_coord
        self.value: Optional[float] = value
    
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

    '''
    def _direction(self) -> Direction:
        x1,y1 = self._start_terminal.x, self._start_terminal.y
        #x1, y1 = self._start_coords
        x2,y2 = self._end_terminal.x, self._end_terminal.y
        #x2, y2 = self._end_coords
        diff_x = x1 - x2
        diff_y = y1 - y2

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

    '''

    '''
    def _direction_terminal(self):
        x1, y1 = self._terminal_start_coords
        x2, y2 = self._terminal_end_coords
        diff_x = x1 - x2
        diff_y = y1 - y2

        match (diff_x, diff_y):
            case (0, diff_y) if diff_y < 0:
                return "down"
            case (0, diff_y) if diff_y > 0:
                return "up"
            case (diff_x, 0) if diff_x < 0:
                return "right"
            case (diff_x, 0) if diff_x > 0:
                return "left"
            case _:
                return "up"   
    '''
    '''
    def _direction_original(self):
        x1, y1 = self._start_coords
        x2, y2 = self._end_coords
        diff_x = x1 - x2
        diff_y = y1 - y2

        match (diff_x, diff_y):
            case (0, diff_y) if diff_y < 0:
                return "down"
            case (0, diff_y) if diff_y > 0:
                return "up"
            case (diff_x, 0) if diff_x < 0:
                return "right"
            case (diff_x, 0) if diff_x > 0:
                return "left"
            case _:
                return "up"          
    '''
    '''
    @property
    def direction(self) -> Direction:
        return self._direction()      
    '''

    @property
    def shouldReverse(self) -> bool:
        return False  

    @property
    def shouldFlip(self) -> bool:
        return False  

    @property
    def component_manifest(self) -> None:
        pass

    def accept(self, d: Drawing, v: Visitor) -> None:
        return v.visit_any(d, self)

