

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional

from .component_warehouse import component_repository
from .drawing_state import DrawingState
from .circuitjsgrammar import CircuitJSGrammar
from .visitor import SchemDrawVisitor
from .point import Point
from .component_manifest import ComponentManifest

class CircuitJSToSchemDraw:
    def __init__(self, input_file:str , output_file:str) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.visitor = SchemDrawVisitor()
        self.grammar = CircuitJSGrammar()
        self.drawing_state = DrawingState()
        self.component_manifests = []
        self.lookup = {}

    def create_component_manifest(self, component_name:str, start_coords: Point, end_coords: Point, value: Optional[float] = None) -> ComponentManifest:    
        return ComponentManifest(component_name, start_coords, end_coords, value)

    def circuitjs_element_class(self, component_manifest):
        component_repo = component_repository()
        element_class = component_repo[component_manifest.component_name]
        return element_class

    def create_lookup(self):
        lookup = defaultdict(list)

        for component_manifest in self.component_manifests:
            #print(component_repo[component_manifest.component_name])
            element_class = self.circuitjs_element_class(component_manifest)
            anchors = element_class.anchors(component_manifest.start_coords, component_manifest.end_coords)
            for anchor, terminal in anchors:
                lookup[terminal].append(  (component_manifest, anchor) )

        return lookup    


    def find_first(self, points):
        return sorted(points).pop()
        #result = points.pop()
        #for point in points:
        #    if point < result:
        #        result = point
        #return result

    def other_anchors(self, component_manifest: ComponentManifest, excluded_anchor):
        element_class = self.circuitjs_element_class(component_manifest)
        anchors = element_class.anchors(component_manifest.start_coords, component_manifest.end_coords)        
        anchors = [(anchor,terminal) for anchor,terminal in anchors if not anchor == excluded_anchor]            
        return anchors

    def parse_input_file(self):
        with open(self.input_file, "r") as f:
            f.readline()
            for line in f:            
                parsing_result = self.grammar.parse(line)
                if parsing_result.is_valid:                
                    component_name, start_terminal, end_terminal, value_literal = self.grammar.extract(parsing_result)        
                    component_manifest = self.create_component_manifest(component_name, start_coords=Point(*start_terminal), end_coords=Point(*end_terminal), value=value_literal)
                    self.component_manifests.append(component_manifest)

    def convert(self) -> None:
        self.parse_input_file()
        #print(component_manifests)
        lookup = self.create_lookup()
        #print(lookup)
        lookup_terminal = self.find_first(list(lookup.keys()))
        print(lookup_terminal)
        drawing_order = []

        drawn_anchors = []
        candidate_anchors = []

        #print(f"number of items in components manifest: {len(self.component_manifests)}")
        for i in range(3):
            terminals = lookup[lookup_terminal]
            if lookup_terminal in candidate_anchors:
                candidate_anchors.remove(lookup_terminal)
            for terminal in terminals:
                drawing_order.append(terminal)
                component_manifest, anchor = terminal
                #self.component_manifests.remove(component_manifest)
                anchors = self.other_anchors(component_manifest, anchor)
                for _, other_terminal in anchors:
                    drawn_anchors.append(lookup_terminal)
                    candidate_anchors.append(other_terminal)
                #     first_terminal = find_first(drawn_anchors)

        #print(drawing_order)
        print(candidate_anchors)
        lookup_terminal = self.find_first(candidate_anchors)
        


