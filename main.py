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

def all_tests():
    max_tests = 9
    for i in range(max_tests):
        circuitjs_to_schemdraw = CircuitJSToSchemDraw(input_file=f"tests/test00{i+1}.txt", output_file=f"out/test00{i+1}.svg")
        circuitjs_to_schemdraw.convert()

def one_test():
    circuitjs_to_schemdraw = CircuitJSToSchemDraw(input_file="tests/test011.txt", output_file="out/test011.svg")
    circuitjs_to_schemdraw.convert()    

if __name__ == "__main__":
    use_matplotlib_backend()
    #use_svg_backend()
    
    #all_tests()
    one_test()

