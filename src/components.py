
#
# Component Repository
#

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import schemdraw.elements as elm

from .point import Point

from .component_warehouse import component_warehouse
from .electronic_component import ElectronicComponent
from .schemdraw_manifest import SchemdrawElementManifest
from .visitor import SchemDrawVisitor
#
# Generic components
#

@dataclass
class Manifest:
  start_coords: Point
  end_coords: Point
  value: Optional[float]

class Direction(Enum):
  up = "up"
  down = "down"
  left = "left"
  right = "right"


class TwoTerminalComponent(ElectronicComponent):
    @classmethod
    def anchors(cls, start_terminal, end_terminal):
        return [
            ("start", start_terminal),
            ("end", end_terminal)
        ]

    def _direction(self):
        diff_x = self.start_coords.x - self.end_coords.x
        diff_y = self.start_coords.y - self.end_coords.y

        match (diff_x, diff_y):
            case (0, diff_y) if diff_y < 0:
                return "down"
            case (0, diff_y) if diff_y > 0:
                #return "up"
                return "down"
            case (diff_x, 0) if diff_x < 0:
                return "right"
            case (diff_x, 0) if diff_x > 0:
                #return "left"
                return "right"
            case _:
                return "up"

    def _direction_original(self):
        diff_x = self.start_coords.x - self.end_coords.x
        diff_y = self.start_coords.y - self.end_coords.y

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

    @property
    def schemdraw_args(self):
        return {"d":self._direction()}

    def to_schemdraw_element(self, visitor: SchemDrawVisitor):
        return visitor.visit_any(self)    

class SingleTerminalComponent(TwoTerminalComponent):
    @classmethod
    def anchors(cls, start_terminal, end_terminal):
        return [
            ("start", start_terminal)            
        ]

    @property
    def has_length(self):
        return False

class TwoTerminalDirectionalComponent(TwoTerminalComponent):
    @property
    def schemdraw_args(self):        
        return {
            "d":self._direction(),
            "reverse": self.shouldReverse
        }
    
    @property
    def shouldReverse(self):
        direction = self._direction_original()
        match direction:
            case 'up'|'left':
                return True
            case _:
                return False
    


class ThreeTerminalComponent(TwoTerminalComponent):
    @property
    def has_length(self):
        return False

    @property
    def wire_length(self):
        diff_x = self.start_coords.x - self.end_coords.x
        diff_y = self.start_coords.y - self.end_coords.y

        default_three_terminal_length = 22.5

        match diff_x, diff_y:
            case (0, diff_y):
                return abs(diff_y) - default_three_terminal_length
              
            case (diff_x, 0):
                return abs(diff_x) - default_three_terminal_length
            case _:
                return 0.0

    @property
    def anchor_coords(self):
        wire_length = self.wire_length
        start_coords = self.start_coords
        wire_end = start_coords + Point(wire_length, 0.0)
        return wire_length, wire_end

    def to_schemdraw_element(self, visitor: SchemDrawVisitor):
        return visitor.visit_three_terminal(self) 

#
# Specific components
#

@component_warehouse.component
class capacitor(TwoTerminalComponent):
    classname = "capacitor"
    class Units(Enum):
        farads = "F"
        microfarads = "µF"
        picofarads = "pF"

    @property
    def schemdraw_element(self) -> type:
        return elm.Capacitor

    @property
    def labelPrefix(self) -> str:
        return "C"

@component_warehouse.component
class ground(SingleTerminalComponent):
    classname = "ground"
    def schemdraw_element(self) -> type:
        return elm.Ground

    @property
    def hasValue(self) -> bool:
        return False

    @property
    def hasLabel(self) ->bool:
        return False

    def _direction(self):
        element_direction = super()._direction()
        match element_direction:
            case 'down':
                return 'right'
            case _:
                return element_direction
    

@component_warehouse.component
class inductor(TwoTerminalComponent):
    classname = "inductor"
    class Units(Enum):
        henry = "H"
        millihenry = "mH"
        microhenry = "µH"
    
    def schemdraw_element(self):
        return elm.Inductor

@component_warehouse.component
class npntransistor(ThreeTerminalComponent):
    classname = "npntransistor"
    def schemdraw_element(self) -> type:
        return elm.transistors.BjtNpn

@component_warehouse.component
class pchannelmosfet(ThreeTerminalComponent):
    classname = "pchannelmosfet"
    def schemdraw_element(self) -> type:
        return elm.transistors.PFet

@component_warehouse.component
class resistor(TwoTerminalComponent):
    classname = "resistor"
    class Units(Enum):
        ohms = "Ω"
        killohms = "kΩ"
        megaohms = "mΩ"

    def schemdraw_element(self) -> type:
        return elm.Resistor

    @property
    def labelPrefix(self) -> str:
        return "R"

@component_warehouse.component
class switch(TwoTerminalComponent):
    classname = "switch"
    def schemdraw_element(self) -> type:
        return elm.Switch

    @property
    def hasValue(self) -> bool:
        return False

    @property
    def hasLabel(self) -> bool:
        return False    

@component_warehouse.component
class voltage(TwoTerminalDirectionalComponent):
    classname = "voltage"
    class Units(Enum):
        volts = "V"

    def schemdraw_element(self) -> type:
        return elm.SourceV

    @property
    def labelPrefix(self) -> str:
        return "V"

    @property
    def isDirectional(self) -> bool:
        return True

@component_warehouse.component
class wire(TwoTerminalComponent):
    classname = "wire"

    @classmethod
    def fromargs(cls, start_coords, end_coords):
        manifest = Manifest(start_coords, end_coords, None)
        return cls(manifest)

    def schemdraw_element(self) -> type:
        return elm.Line

    @property
    def hasValue(self) -> bool:
        return False

    @property
    def hasLabel(self) -> bool:
        return False

