from dataclasses import dataclass
from typing import List

@dataclass
class TourEntity:
    name: str
    country: str
    price: float
    rating: float
    description: str
    attributes: List[str]
    duration: str
    included: str
    image_url: str
    hotel_stars: str 
    season: str