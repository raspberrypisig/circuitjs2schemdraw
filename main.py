
from collections import defaultdict
import schemdraw
from visitor import SchemDrawVisitor
from circuitjsgrammar import CircuitJSGrammar
from point import Point

schemdraw.use('svg')
schemdraw.svgconfig.text = 'path'
schemdraw.svgconfig.svg2 = False
schemdraw.svgconfig.precision = 2

class DrawingState:
    def __init__(self) -> None:
        self._lookup = defaultdict(list)
        self._elements_to_draw = []
        self._elements_drawn = []
        self._candidate_coords = []
        self._drawn_list = {}
        self._number_of_elements = 0

def main(input_file: str, output_file: str) -> None:
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

if __name__ == "__main__":
    main("tests/test001.txt", "out/test001.svg")   
'''
max_test_number = 5
for i in range(max_test_number):
    num = str(i+1).zfill(3) 
    input_file = f"tests/test{num}.txt"
    output_file = f"out/test{num}.svg"
    main(input_file, output_file)        
'''

