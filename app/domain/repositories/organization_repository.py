from abc import ABC, abstractmethod
from typing import Optional, Tuple, Sequence
from app.infrastructure.database.models.organization import Organization


class IOrganizationRepository(ABC):

    @abstractmethod
    async def get_by_id(self, organization_id: int) -> Optional[Organization]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_name(self, name: Optional[str], page: int, page_size: int) -> Tuple[int, Sequence[Organization]]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_activity(self, activity_id: int, page: int, page_size: int) -> Tuple[int, Sequence[Organization]]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_building(self, building_id: int, page: int, page_size: int) -> Tuple[int, Sequence[Organization]]:
        raise NotImplementedError
