

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional
import schemdraw

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

    def element_class(self, component_manifest):
        component_repo = component_repository()
        element_class = component_repo[component_manifest.component_name]
        return element_class

    def create_lookup(self):
        lookup = defaultdict(list)

        for component_manifest in self.component_manifests:
            #print(component_repo[component_manifest.component_name])
            element_class = self.element_class(component_manifest)
            anchors = element_class.anchors(component_manifest.start_coords, component_manifest.end_coords)
            for anchor, terminal in anchors:
                lookup[terminal].append(  (component_manifest, anchor) )

        return lookup    


    def find_first(self, points):
        return next(iter(sorted(points)))

    def other_anchors(self, component_manifest: ComponentManifest, excluded_anchor):
        element_class = self.element_class(component_manifest)
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

    def visit(self, manifests):
        schemdraw_elements = []
        for coord, manifest_group in manifests:
            #print("push")
            schemdraw_group = []
            for component_manifest in manifest_group:
                #print(component_manifest)
                element_class = self.element_class(component_manifest)
                schemdraw_element = element_class(component_manifest).to_schemdraw_element(self.visitor)
                schemdraw_group.append(schemdraw_element)
            #print("pop")
            schemdraw_elements.append((coord, schemdraw_group))
        return schemdraw_elements

    def draw(self, elements):


        starting_point,_ = elements[0]
        print(starting_point)

        scale_factor = 30.0
        def drawing_coords(coord):
            return ((coord.x - starting_point.x)/scale_factor, (starting_point.y - coord.y )/scale_factor)

        def component_length(start_coord, end_coord):
            diff_x = start_coord.x - end_coord.x
            diff_y = start_coord.y - end_coord.y

            match diff_x, diff_y:
                case (0, _):
                  return abs(diff_y)/scale_factor
                case (_, 0):
                  return abs(diff_x)/scale_factor
                case _:
                    return -1.0
            #return abs(p1 - p2)/scale_factor

        draw_lookup = {}

        with schemdraw.Drawing(file=self.output_file, show=False) as d:
            d.config(fontsize=14.0, lw=2)

            for lookup_terminal, element in elements:
                
                #if lookup_terminal in draw_lookup:
                #    here = draw_lookup[lookup_terminal]
                #    d.move(here.x, here.y)
                for component in element:                    
                    start_coord = component.start_coord
                    end_coord = component.end_coord
                    length = component_length(start_coord, end_coord)
                    current_point_x, current_point_y = drawing_coords(start_coord)
                    #print(start_coord, end_coord)                    
                    d.push()
                    #print("what value now:", d.here)
                    c = component.element_class()
                    
                    if type(c) == type:
                        e = component.element_class()(**component.constructor_args)

                    else:
                        e = component.element_class(**component.constructor_args)
          
                    if component.has_length:
                        d += e.at([current_point_x, current_point_y]).length(length)
                        
                    else:
                        d += e.at([current_point_x, current_point_y])

                    draw_lookup[component.end_coord] =  d.here
                    d.pop()
        print(draw_lookup)            
                    

    def convert(self) -> None:
        self.parse_input_file()
        #print(component_manifests)
        lookup = self.create_lookup()
        #print(lookup)
        lookup_terminal = self.find_first(list(lookup.keys()))
        #print("first", lookup_terminal)
        drawing_order = []

        drawn_anchors = []
        candidate_anchors = []

        #print(f"number of items in components manifest: {len(self.component_manifests)}")
        #for i in range(len(lookup.keys())):
        while not len(self.component_manifests) == len([item for _, sublist in drawing_order for item in sublist]):
            terminals = lookup[lookup_terminal]
            sub_drawing_order = []
            for terminal in terminals:                
                component_manifest, anchor = terminal   
                if component_manifest in [item for _, sublist in drawing_order for item in sublist]:
                    continue

                sub_drawing_order.append(component_manifest)                         
                anchors = self.other_anchors(component_manifest, anchor)
                for _, other_terminal in anchors:                    
                    drawn_anchors.append(lookup_terminal)
                    candidate_anchors.append(other_terminal)
                #     first_terminal = find_first(drawn_anchors)
            drawing_order.append((lookup_terminal, sub_drawing_order))
            lookup_terminal = self.find_first(candidate_anchors)
            #print("next",lookup_terminal)
            candidate_anchors.remove(lookup_terminal)
            #print("remaining anchors", candidate_anchors)
        #print(drawing_order)
        #print(len(drawing_order))
        #print(candidate_anchors)
        elements = self.visit(drawing_order)
        #print(elements)
        self.draw(elements)        
       


