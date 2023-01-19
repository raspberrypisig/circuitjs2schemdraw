from typing import Any, Optional
from pyleri import (
    Choice,
    Grammar,
    Keyword,
    Regex,
    Repeat,
    Sequence)

class CircuitJSGrammar(Grammar): 
    number_literal = Regex('[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?')
    start_terminal_coords = Repeat(number_literal, mi=2, ma=2)
    end_terminal_coords = Repeat(number_literal, mi=2, ma=2)
    two_terminal_coords = Sequence(start_terminal_coords, end_terminal_coords)
    booly = Choice(Keyword('true'), Keyword('false'))
    string_literal = Regex('[A-Za-z0-9_]+') 
    value_literal = Sequence(number_literal)

    capacitor = Sequence(Keyword('c'), two_terminal_coords, number_literal, value_literal, Repeat(number_literal, mi=2, ma=2))
    ground = Sequence(Keyword('g'), two_terminal_coords, Repeat(number_literal, mi=2, ma=2))    
    inductor = Sequence(Keyword('l'),  two_terminal_coords, number_literal, value_literal, Repeat(number_literal, mi=2, ma=2))
    npntransistor = Sequence(Keyword('t'), two_terminal_coords, Repeat(number_literal, mi=5, ma=5), string_literal)
    pchannelmosfet = Sequence(Keyword('f'), two_terminal_coords, Repeat(number_literal, mi=3, ma=3))
    resistor = Sequence(Keyword('r'), two_terminal_coords, number_literal, value_literal)
    switch = Sequence(Keyword('s'), two_terminal_coords, number_literal, number_literal, booly)
    voltage = Sequence(Keyword('v'), two_terminal_coords, Repeat(number_literal, mi=3, ma=3), value_literal, Repeat(number_literal, mi=2, ma=2), number_literal)
    wire = Sequence(Keyword('w'), two_terminal_coords, number_literal)

    START = Choice(capacitor, ground, inductor, npntransistor, pchannelmosfet, resistor, switch, voltage, wire)

    def _create_simple_node(self, tree) -> dict[str, str]:
        return {
            "name": tree.element.name if hasattr(tree.element, 'name') else None,
            "element": tree.element.__class__.__name__,
            'string': tree.string            
        }

    def find(self, tree: Any, search: dict[str, str], result_field: str) -> Optional[str]:

        #mytree: dict = {s: getattr(tree, s) for s in tree.__slots__}
        #print(mytree)

        simple_node = self._create_simple_node(tree)

        if simple_node | search == simple_node:
            return simple_node[result_field]

        if tree is None:
            return None

        for child in tree.children:
            simple_child_node = self._create_simple_node(child)           
            if simple_child_node | search == simple_child_node:
                return simple_child_node[result_field]
            else:
                for subchild in child.children:
                    result = self.find(subchild, search, result_field)
                    if result is not None:
                        return result
        return None
        
        
    def extract(self, parsing_result):
        component_name: Optional[str] =  self.find(parsing_result.tree, search={"element": "Sequence"}, result_field="name")    
        
        start_terminal = self.find(parsing_result.tree, search={"name": "start_terminal_coords"}, result_field="string").split(" ")
        end_terminal =   self.find(parsing_result.tree, search={"name": "end_terminal_coords"}, result_field="string").split(" ")
        value_literal = self.find(parsing_result.tree, search={"name": "value_literal"}, result_field="string")
        if value_literal:
            component_value = value_literal.split().pop()
        else:
            component_value = None

        return component_name, list(map(int, start_terminal)),  list(map(int, end_terminal)), component_value
        

        

