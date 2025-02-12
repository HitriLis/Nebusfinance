from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from app.infrastructure.database.models.organization import Organization


class IOrganizationRepository(ABC):

    @abstractmethod
    async def get_by_id(self, organization_id: int) -> Optional[Organization]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_name(self, name: Optional[str], page: int, page_size: int) -> Tuple[int, List[Organization]]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_activity(self, activity_ids: List[int], page: int, page_size: int) -> Tuple[int, List[Organization]]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_building(self, building_id: int, page: int, page_size: int) -> Tuple[int, List[Organization]]:
        raise NotImplementedError

    @abstractmethod
    async def list_organization_within_radius(self,
                                              latitude: float,
                                              longitude: float,
                                              radius: float,
                                              page: int,
                                              page_size: int
                                              ) -> Tuple[int, List[Organization]]:
        raise NotImplementedError

    async def list_organization_within_rectangle(self,
                                                 lat_min: float,
                                                 lon_min: float,
                                                 lat_max: float,
                                                 lon_max: float,
                                                 page: int,
                                                 page_size: int
                                                 ) -> Tuple[int, List[Organization]]:
        raise NotImplementedError


