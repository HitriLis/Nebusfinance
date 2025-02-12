from abc import ABC, abstractmethod
from typing import List


class IActivityRepository(ABC):
    @abstractmethod
    async def get_activity_ids(self, activity_id: int) -> List[int]:
        raise NotImplementedError
