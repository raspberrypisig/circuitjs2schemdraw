
from collections import defaultdict
import schemdraw
from src.visitor import SchemDrawVisitor
from src.circuitjsgrammar import CircuitJSGrammar
from src.point import Point

schemdraw.use('svg')
schemdraw.svgconfig.text = 'path'
schemdraw.svgconfig.svg2 = False
schemdraw.svgconfig.precision = 2

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

