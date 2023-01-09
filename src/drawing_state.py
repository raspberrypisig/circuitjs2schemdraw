

from collections import defaultdict
from typing import Any


class DrawingState:
    def __init__(self) -> None:
        self._lookup:Any = defaultdict(list)
        self._elements_to_draw = []
        self._elements_drawn = []
        self._candidate_coords = []
        self._drawn_list = {}
        self._number_of_elements = 0

