from abc import ABC, abstractmethod
from typing import List, Self
from enum import Enum
import schemdraw

schemdraw.use('svg')
schemdraw.svgconfig.text = 'path'
schemdraw.svgconfig.svg2 = False
schemdraw.svgconfig.precision = 2

def main(input_file: str, output_file: str) -> None:
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

