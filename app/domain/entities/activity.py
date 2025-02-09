from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Activity:
    id: int
    name: str
    parent_id: Optional[int] = None
    children: List["Activity"] = None
