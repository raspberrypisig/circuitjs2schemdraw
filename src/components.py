
#
# Component Repository
#

from enum import Enum
import schemdraw.elements as elm

from .component_warehouse import component_warehouse
from .electronic_component import ElectronicComponent

#
# Generic components
#

class TwoTerminalComponent(ElectronicComponent):
    def setValue(self, parsing_element: Any) -> None:
        self._value = parsing_element[3].string
        print(self._value)
        
class TwoTerminalDirectionalComponent(TwoTerminalComponent):
    @property
    def shouldReverse(self):
        direction = self._direction_terminal()
        match direction:
            case 'up'|'left':
                return True
            case _:
                return False

class ThreeTerminalComponent(ElectronicComponent):
    pass

#
# Specific components
#

@component_warehouse.component
class capacitor(TwoTerminalComponent):
    class Units(Enum):
        farads = "F"
        microfarads = "µF"
        picofarads = "pF"

    def getElement(self):
        return elm.Capacitor

    @property
    def labelPrefix(self):
        return "C"

@component_warehouse.component
class ground(ElectronicComponent):
    def getElement(self):
        return elm.Ground

    @property
    def hasValue(self):
        return False

    @property
    def hasLabel(self):
        return False

    @property
    def direction(self):
        element_direction = self._direction()
        match element_direction:
            case 'down':
                return 'right'
            case _:
                return element_direction

@component_warehouse.component
class inductor(TwoTerminalComponent):
    class Units(Enum):
        henry = "H"
        millihenry = "mH"
        microhenry = "µH"
    
    def getElement(self):
        return elm.Inductor

@component_warehouse.component
class npntransistor(TwoTerminalComponent):
    def getElement(self):
        return elm.transistors.BjtNpn

@component_warehouse.component
class pchannelmosfet(TwoTerminalComponent):
    def getElement(self):
        return elm.transistors.PFet

@component_warehouse.component
class resistor(TwoTerminalComponent):
    class Units(Enum):
        ohms = "Ω"
        killohms = "kΩ"
        megaohms = "mΩ"

    def getElement(self):
        return elm.Resistor

    @property
    def labelPrefix(self):
        return "R"

@component_warehouse.component
class switch(TwoTerminalComponent):
    def getElement(self):
        return elm.Switch

    @property
    def hasValue(self):
        return False

    @property
    def hasLabel(self):
        return False    

@component_warehouse.component
class voltage(TwoTerminalDirectionalComponent):
    class Units(Enum):
        volts = "V"

    def getElement(self):
        return elm.SourceV

    @property
    def labelPrefix(self):
        return "V"

    @property
    def isDirectional(self):
        return True

@component_warehouse.component
class wire(ElectronicComponent):
    def getElement(self):
        return elm.Line

    @property
    def hasValue(self):
        return False

    @property
    def hasLabel(self):
        return False





