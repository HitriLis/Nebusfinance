from dataclasses import dataclass, field
from typing import Optional, List, TypeVar, Generic

T = TypeVar('T')


@dataclass
class PaginatedResult(Generic[T]):
    data: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int = field(init=False)
    next_page: Optional[int] = field(init=False)
    prev_page: Optional[int] = field(init=False)

    def __post_init__(self):
        """Автоматически вычисляет `total_pages`, `next_page` и `prev_page`."""
        self.total_pages = (self.total + self.page_size - 1) // self.page_size
        self.next_page = self.page + 1 if self.page < self.total_pages else None
        self.prev_page = self.page - 1 if self.page > 1 else None
