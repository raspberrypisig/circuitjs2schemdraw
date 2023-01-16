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
    
    #circuitjs_to_schemdraw = CircuitJSToSchemDraw(input_file="tests/test008.txt", output_file="out/test008.svg")
    #circuitjs_to_schemdraw.convert()


