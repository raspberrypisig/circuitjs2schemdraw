import schemdraw
from src.circuitjs_to_schemdraw import CircuitJSToSchemDraw

# default backend
def use_matplotlib_backend() -> None:
    pass

def use_svg_backend():
    schemdraw.use('svg')
    schemdraw.svgconfig.text = 'path'
    schemdraw.svgconfig.svg2 = False
    schemdraw.svgconfig.precision = 2

if __name__ == "__main__":
    #use_matplotlib_backend()
    use_svg_backend()
    max_tests = 8
    for i in range(max_tests):
        circuitjs_to_schemdraw = CircuitJSToSchemDraw(input_file=f"tests/test00{i+1}.txt", output_file=f"out/test00{i+1}.svg")
        circuitjs_to_schemdraw.convert()
    #circuitjs_to_schemdraw("tests/test007.txt", "out/test007.svg")   
    #circuitjs_to_schemdraw = CircuitJSToSchemDraw(input_file="tests/test007.txt", output_file="out/test007.svg")
    #circuitjs_to_schemdraw.convert()
'''
max_test_number = 5
for i in range(max_test_number):
    num = str(i+1).zfill(3) 
    input_file = f"tests/test{num}.txt"
    output_file = f"out/test{num}.svg"
    main(input_file, output_file)        
'''

