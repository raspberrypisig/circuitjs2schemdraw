from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __eq__(self, o: Self) -> bool:
        return self.x == o.x and self.y == o.y

    def __lt__(self, o:Self) -> bool:
        return self.y < o.y or (self.y == o.y and self.x < o.x) 



