import schemdraw
from src.circuitjs_to_schemdraw import circuitjs_to_schemdraw

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
    circuitjs_to_schemdraw("tests/test001.txt", "out/test001.svg")   
    
'''
max_test_number = 5
for i in range(max_test_number):
    num = str(i+1).zfill(3) 
    input_file = f"tests/test{num}.txt"
    output_file = f"out/test{num}.svg"
    main(input_file, output_file)        
'''

