from typing import Any, Optional
from pyleri import (
    Choice,
    Grammar,
    Keyword,
    Regex,
    Repeat,
    Ref,
    Sequence)


class CircuitJSGrammar(Grammar):
    START = Ref()
    
    number_literal = Regex('[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?')
    two_terminal_coords = Repeat(number_literal, mi=4, ma=4)
    booly = Choice(Keyword('true'), Keyword('false'))
    string_literal = Regex('[A-Za-z0-9_]+') 

    capacitor = Sequence(Keyword('c'), two_terminal_coords, number_literal, number_literal, Repeat(number_literal, mi=2, ma=2))
    ground = Sequence(Keyword('g'), two_terminal_coords, Repeat(number_literal, mi=2, ma=2))    
    inductor = Sequence(Keyword('l'),  two_terminal_coords, number_literal, number_literal, Repeat(number_literal, mi=2, ma=2))
    npntransistor = Sequence(Keyword('t'), two_terminal_coords, Repeat(number_literal, mi=5, ma=5), string_literal)
    pchannelmosfet = Sequence(Keyword('f'), two_terminal_coords, Repeat(number_literal, mi=4, ma=4))
    resistor = Sequence(Keyword('r'), two_terminal_coords, number_literal, number_literal)
    switch = Sequence(Keyword('s'), two_terminal_coords, number_literal, number_literal, booly)
    voltage = Sequence(Keyword('v'), two_terminal_coords, Repeat(number_literal, mi=3, ma=3), number_literal, Repeat(number_literal, mi=2, ma=2), number_literal)
    wire = Sequence(Keyword('w'), two_terminal_coords, number_literal)

    START = Choice(capacitor, ground, inductor, npntransistor, pchannelmosfet, resistor, switch, voltage, wire)


    def _create_simple_node(self, tree) -> None:
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
            #mychild = {s: getattr(child, s) for s in child.__slots__ if hasattr(child, s)}
            if simple_child_node | search == simple_child_node:
                return simple_child_node[result_field]
            else:
                for subchild in child.children:
                    result = self.find(subchild, search, result_field)
                    if result is not None:
                        return result
        return None
        
        
    