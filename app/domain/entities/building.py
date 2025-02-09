from dataclasses import dataclass
from typing import Optional


@dataclass
class Building:
    id: int
    address: str
    latitude: float
    longitude: float
