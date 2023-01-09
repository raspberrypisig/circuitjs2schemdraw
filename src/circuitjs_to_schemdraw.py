

from .drawing_state import DrawingState
from .circuitjsgrammar import CircuitJSGrammar
from .visitor import SchemDrawVisitor


def circuitjs_to_schemdraw(input_file: str, output_file: str) -> None:
    visitor = SchemDrawVisitor()
    grammar = CircuitJSGrammar()
    drawing_state = DrawingState()
    
    with open(input_file, "r") as f:
        f.readline()
        for line in f:            
            parsing_result = grammar.parse(line)
            #print(parsing_result.is_valid)
            if parsing_result.is_valid:
                pass    
