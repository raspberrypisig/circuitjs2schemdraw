

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

    def create_lookup(self):
        component_repo = component_repository()
        lookup = defaultdict(list)

        for component_manifest in self.component_manifests:
            #print(component_repo[component_manifest.component_name])
            element_class = component_repo[component_manifest.component_name]
            anchors = element_class.anchors(component_manifest.start_coords, component_manifest.end_coords)
            for anchor, terminal in anchors:
                lookup[terminal].append(  (component_manifest, anchor) )

        return lookup    


    def find_first(self, points):
        result = points.pop()
        for point in points:
            if point < result:
                result = point
        return result

    def convert(self) -> None:
        with open(self.input_file, "r") as f:
            f.readline()
            for line in f:            
                parsing_result = self.grammar.parse(line)
                if parsing_result.is_valid:                
                    component_name, start_terminal, end_terminal, value_literal = self.grammar.extract(parsing_result)        
                    component_manifest = self.create_component_manifest(component_name, start_coords=Point(*start_terminal), end_coords=Point(*end_terminal), value=value_literal)
                    self.component_manifests.append(component_manifest)
        
        #print(component_manifests)
        lookup = self.create_lookup()
        #print(lookup)
        lookup_terminal = self.find_first(list(lookup.keys()))
        #print(first_terminal)
        drawing_order = []

        drawn_anchors = []
        candidate_anchors = set([])

        print(f"number of items in components manifest: {len(self.component_manifests)}")
        for i in range(1):
            terminals = lookup[lookup_terminal]
            for terminal in terminals:
                drawing_order.append(terminal)
                component_manifest, anchor = terminal
                print(component_manifest)
                print(anchor)
                self.component_manifests.remove(component_manifest)
                print(f"number of items in components manifest: {len(self.component_manifests)}")
                #anchors = get_anchors(component_manifest)
                # for other_anchor in anchors:
                #     drawn_anchors.append(lookup_terminal)
                #     candidate_anchors.append(anchors[other])
                #     first_terminal = find_first(drawn_anchors)

        print(drawing_order)

