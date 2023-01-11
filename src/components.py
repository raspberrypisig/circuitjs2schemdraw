
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
    def setValue(self, parsing_element: any) -> None:
        self._value = float(parsing_element[3].string)
        print(self._value)
        
class TwoTerminalDirectionalComponent(TwoTerminalComponent):
    pass
    '''
    @property
    def shouldReverse(self):
        direction = self._direction_terminal()
        match direction:
            case 'up'|'left':
                return True
            case _:
                return False
    '''
class ThreeTerminalComponent(ElectronicComponent):
    pass

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

    def getElement(self) -> type:
        return elm.Capacitor

    @property
    def labelPrefix(self) -> str:
        return "C"

@component_warehouse.component
class ground(ElectronicComponent):
    classname = "ground"
    def getElement(self) -> type:
        return elm.Ground

    @property
    def hasValue(self) -> bool:
        return False

    @property
    def hasLabel(self) ->bool:
        return False

    '''
    @property
    def direction(self):
        element_direction = self._direction()
        match element_direction:
            case 'down':
                return 'right'
            case _:
                return element_direction
    '''

@component_warehouse.component
class inductor(TwoTerminalComponent):
    classname = "inductor"
    class Units(Enum):
        henry = "H"
        millihenry = "mH"
        microhenry = "µH"
    
    def getElement(self):
        return elm.Inductor

@component_warehouse.component
class npntransistor(TwoTerminalComponent):
    classname = "npntransistor"
    def getElement(self) -> type:
        return elm.transistors.BjtNpn

@component_warehouse.component
class pchannelmosfet(TwoTerminalComponent):
    classname = "pchannelmosfet"
    def getElement(self) -> type:
        return elm.transistors.PFet

@component_warehouse.component
class resistor(TwoTerminalComponent):
    classname = "resistor"
    class Units(Enum):
        ohms = "Ω"
        killohms = "kΩ"
        megaohms = "mΩ"

    def getElement(self) -> type:
        return elm.Resistor

    @property
    def labelPrefix(self) -> str:
        return "R"



@component_warehouse.component
class switch(TwoTerminalComponent):
    classname = "switch"
    def getElement(self) -> type:
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

    def getElement(self) -> type:
        return elm.SourceV

    @property
    def labelPrefix(self) -> str:
        return "V"

    @property
    def isDirectional(self) -> bool:
        return True

@component_warehouse.component
class wire(ElectronicComponent):
    classname = "wire"
    def getElement(self) -> type:
        return elm.Line

    @property
    def hasValue(self) -> bool:
        return False

    @property
    def hasLabel(self) -> bool:
        return False





