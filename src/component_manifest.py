from dataclasses import dataclass
from typing import Optional
from .point import Point

@dataclass
class ComponentManifest:
    component_name: str
    start_coords: Point
    end_coords: Point
    value: Optional[float]