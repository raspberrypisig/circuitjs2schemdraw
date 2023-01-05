from pyleri import (
    Choice,
    Grammar,
    Keyword,
    List,
    Optional,
    Regex,
    Repeat,
    Ref,
    Sequence,
)
import json
import schemdraw
import schemdraw.elements as elm
from collections import defaultdict


class CircuitJSGrammar(Grammar):
    START = Ref()

    # integer_literal = Regex('[0-9]+')
    # decimal_literal = Regex('([+-]?\d*\.\d+)')
    # exponential_literal = Regex('(\d*\.\d+|\d+)(e[+-]?\d+)?')

    # exponential_or_decimal_literal = Choice(exponential_literal, decimal_literal)
    # integer_or_decimal_literal = Choice(integer_literal, decimal_literal)
    number_literal = Regex("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
    two_terminal_coords = Repeat(number_literal, mi=4, ma=4)
    booly = Choice(Keyword("true"), Keyword("false"))

    capacitor = Sequence(
        Keyword("c"),
        two_terminal_coords,
        number_literal,
        number_literal,
        Repeat(number_literal, mi=2, ma=2),
    )
    ground = Sequence(
        Keyword("g"), two_terminal_coords, Repeat(number_literal, mi=2, ma=2)
    )
    inductor = Sequence(
        Keyword("l"),
        two_terminal_coords,
        number_literal,
        number_literal,
        Repeat(number_literal, mi=2, ma=2),
    )
    resistor = Sequence(
        Keyword("r"), two_terminal_coords, number_literal, number_literal
    )
    switch = Sequence(
        Keyword("s"), two_terminal_coords, number_literal, number_literal, booly
    )
    voltage = Sequence(
        Keyword("v"),
        two_terminal_coords,
        Repeat(number_literal, mi=3, ma=3),
        number_literal,
        Repeat(number_literal, mi=2, ma=2),
        number_literal,
    )
    wire = Sequence(Keyword("w"), two_terminal_coords, number_literal)

    START = Choice(capacitor, ground, inductor, resistor, switch, voltage, wire)
    # START = Choice(capacitor, resistor, switch, voltage, wire)


def node_props(node, children):
    return {
        "start": node.start,
        "end": node.end,
        "name": node.element.name if hasattr(node.element, "name") else None,
        "element": node.element.__class__.__name__,
        "string": node.string,
        "children": children,
    }


# Recursive method to get the children of a node object:
def get_children(children):
    return [node_props(c, get_children(c.children)) for c in children]


# View the parse tree:
def view_parse_tree(res):
    start = res.tree.children[0] if res.tree.children else res.tree
    return node_props(start, get_children(start.children))


class ComponentWarehouse:
    def __init__(self):
        self.classes = {}

    def add_class(self, c):
        self.classes[c.__name__] = c

    # -- the decorator
    def component(self, c):
        self.add_class(c)

        # Decorators have to return the function/class passed (or a modified variant thereof), however I'd rather do this separately than retroactively change add_class, so.
        # "held" is more succint, anyway.
        return c

    def __getitem__(self, n):
        return self.classes[n]


component_warehouse = ComponentWarehouse()


class ElectricComponent(object):

    id = 1

    def __init__(self):
        self._direction = "up"

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    def corrected_direction(self, dir):
        match (self.direction, dir):
            case ("left", "down"):
                return "right"
            case _:
                return "up"

    @property
    def hasValue(self):
        return True

    @property
    def anchor(self):
        return ["start", "end"]

    @property
    def hasLabel(self):
        return True

    @property
    def getLabel(self):
        return self.id

    @property
    def isDirectional(self):
        return False


class TwoTerminalComponent(ElectricComponent):
    def setValue(self, parsing_element):
        self._value = parsing_element[3].string
        print(self._value)


@component_warehouse.component
class capacitor(TwoTerminalComponent):
    def getElement(self):
        return elm.Capacitor()

    @property
    def labelPrefix(self):
        return "C"

    @property
    def valueUnits(self):
        return "F"


@component_warehouse.component
class ground(ElectricComponent):
    def getElement(self):
        return elm.Ground()

    @property
    def hasValue(self):
        return False

    @property
    def hasLabel(self):
        return False


@component_warehouse.component
class resistor(TwoTerminalComponent):
    def getElement(self):
        return elm.Resistor()

    @property
    def labelPrefix(self):
        return "R"

    @property
    def valueUnits(self):
        return "Ω"


@component_warehouse.component
class inductor(TwoTerminalComponent):
    def getElement(self):
        return elm.Inductor()


@component_warehouse.component
class switch(TwoTerminalComponent):
    def getElement(self):
        return elm.Switch()

    @property
    def hasValue(self):
        return False

    @property
    def hasLabel(self):
        return False


@component_warehouse.component
class voltage(TwoTerminalComponent):
    def getElement(self):
        return elm.SourceV()

    @property
    def labelPrefix(self):
        return "V"

    @property
    def valueUnits(self):
        return "V"

    @property
    def isDirectional(self):
        return True


@component_warehouse.component
class wire(ElectricComponent):
    def getElement(self):
        return elm.Line()

    @property
    def hasValue(self):
        return False

    @property
    def hasLabel(self):
        return False


def getCoordinates(parsing_element):
    coords = parsing_element.split()
    return [(int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3]))]


def getDirection(coords):
    first_terminal, second_terminal = coords
    x1, y1 = first_terminal
    x2, y2 = second_terminal
    diff_x = int(x1) - int(x2)
    diff_y = int(y1) - int(y2)

    match (diff_x, diff_y):
        case (0, diff_y) if diff_y < 0:
            return "down"
        case (0, diff_y) if diff_y > 0:
            return "up"
        case (diff_x, 0) if diff_x < 0:
            return "right"
        case (diff_x, 0) if diff_x > 0:
            return "left"
        case _:
            return "up"


input_file = "tests/basic2.txt"
output_file = "out.svg"


if __name__ == "__main__":
    grammar = CircuitJSGrammar()

    lookup = {}
    elements_to_draw = []
    elements_drawn = []

    def parse_component(parsing_result):
        start = parsing_result.tree.children[0].children[0]
        component_name = start.element.name
        coordinates = start.children[1].string
        terminal_coords = getCoordinates(coordinates)
        sorted_coordinates = sorted(terminal_coords, key=lambda x: (x[0], int(x[1])))
        start_coords, end_coords = sorted_coordinates
        return {
            "component_name": component_name,
            "terminal_coords": terminal_coords,
            "sorted_coordinates": sorted_coordinates,
            "start_coords": start_coords,
            "end_coords": end_coords,
        }

    def find_left_corner_most(elements):
        leftcorner_most = elements[0]["sorted_coordinates"][0]
        for element in elements[1:]:
            sorted_coordinates = element["sorted_coordinates"]
            lowest_coordinate = sorted_coordinates[0]
            if lowest_coordinate == leftcorner_most:
                continue
            boo = [leftcorner_most, sorted_coordinates[0]]
            sorted_boo = sorted(boo, key=lambda x: (int(x[1]), int(x[0])))
            if boo != sorted_boo:
                leftcorner_most = lowest_coordinate

        return leftcorner_most

    def draw_now(coords, lookup, done_elements):
        print(coords)

    with open(input_file, "r") as f:
        f.readline()
        for line in f:
            # print(line)
            parsing_result = grammar.parse(line)
            # print(parsing_result.is_valid)
            if parsing_result.is_valid:
                component = parse_component(parsing_result)
                # print(component)
                elements_to_draw.append(component)
                lookup[component["start_coords"]] = (component, "start")
                lookup[component["end_coords"]] = (component, "end")

    # print("------------elements--------------\n", elements_to_draw)
    # print("------------lookup----------------\n", lookup)
    coords = find_left_corner_most(elements_to_draw)
    print("------------corner most coord--------\n", coords)
    elements_to_draw_now = draw_now(coords, elements_drawn, lookup)
