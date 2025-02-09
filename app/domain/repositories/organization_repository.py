from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.organization import Organization


class IOrganizationRepository(ABC):

    @abstractmethod
    def get_by_id(self, organization_id: int) -> Organization:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: Optional[str] = None, offset: int = 0, limit: int = 10) -> List[Organization]:
        raise NotImplementedError

    @abstractmethod
    def get_by_activity(self, activity_id: int, offset: int = 0, limit: int = 10) -> List[Organization]:
        raise NotImplementedError

    @abstractmethod
    def get_by_building(self, building_id: int, offset: int = 0, limit: int = 10) -> List[Organization]:
        raise NotImplementedError
