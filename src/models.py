from dataclasses import dataclass
from typing import List

@dataclass
class TourEntity:
    name: str
    attributes: List[str]
    price: float = 0.0

    def __str__(self):
        return f"{self.name} ({', '.join(self.attributes)})"
