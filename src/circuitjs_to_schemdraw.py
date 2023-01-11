

from dataclasses import dataclass
from typing import List, Optional

from .component_warehouse import component_repository
from .drawing_state import DrawingState
from .circuitjsgrammar import CircuitJSGrammar
from .visitor import SchemDrawVisitor
from .point import Point


@dataclass
class ComponentManifest:
    component_name: str
    start_coords: Point
    end_coords: Point
    value: Optional[float]

def create_component_manifest(component_name:str, start_coords: Point, end_coords: Point, value: Optional[float] = None) -> ComponentManifest:    
    return ComponentManifest(component_name, start_coords, end_coords, value)



def create_lookup(component_manifests: List[ComponentManifest]):
    component_repo = component_repository()
    
    for component_manifest in component_manifests:
        print(component_repo[component_manifest.component_name])


def circuitjs_to_schemdraw(input_file: str, output_file: str) -> None:
    visitor = SchemDrawVisitor()
    grammar = CircuitJSGrammar()
    drawing_state = DrawingState()
    component_manifests = []
    lookup = {}

    with open(input_file, "r") as f:
        f.readline()
        for line in f:            
            parsing_result = grammar.parse(line)
            if parsing_result.is_valid:                
                component_name, start_terminal, end_terminal, value_literal = grammar.extract(parsing_result)        
                component_manifest = create_component_manifest(component_name, start_coords=Point(*start_terminal), end_coords=Point(*end_terminal), value=value_literal)
                component_manifests.append(component_manifest)
    
    #print(component_manifests)
    lookup = create_lookup(component_manifests)

    