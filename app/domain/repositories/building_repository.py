from abc import ABC, abstractmethod
from typing import List
from ..entities.building import Building


class IBuildingRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Building]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, building_id: int) -> Building:
        raise NotImplementedError
