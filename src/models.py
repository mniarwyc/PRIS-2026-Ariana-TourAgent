from dataclasses import dataclass, field
from typing import List
@dataclass
class TourEntity:
    name: str
    attributes: List[str]
    price: float = 0.0

    def __str__(self):
        return f"{self.name} ({', '.join(self.attributes)})"


@dataclass
class TourEntity:
    name: str
    attributes: List[str] = field(default_factory=list)
    price: float = 0.0
    rating: float = 0.0  # Новое поле: рейтинг отеля/направления
    description: str = "" # Новое поле: краткое описание

    def __str__(self):
        return f"{self.name} (Рейтинг: {self.rating}, Цена: {self.price}$)"