from dataclasses import dataclass
from typing import List
from .activity import Activity
from .building import Building


@dataclass
class PhoneNumber:
    id: int
    number: str


@dataclass
class Organization:
    id: int
    name: str
    building: Building
    phone_numbers: List[PhoneNumber]
    activities: List[Activity]
