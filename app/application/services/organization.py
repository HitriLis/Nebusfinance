from typing import Optional

from geoalchemy2.shape import to_shape
from app.infrastructure.database.models import Organization as OrganizationModel
from ...domain.entities.organization import Organization, PhoneNumber
from ...domain.entities.activity import Activity
from ...domain.entities.building import Building
from ...domain.entities.paginated_result import PaginatedResult
from ...domain.repositories.organization_repository import IOrganizationRepository
from ...domain.repositories.activity_repository import IActivityRepository


class OrganizationService:
    def __init__(self, organizations_repo: IOrganizationRepository, activity_repo: IActivityRepository):
        self.organizations_repo = organizations_repo
        self.activity_repo = activity_repo

    async def search_organizations(self, name: Optional[str], page: int, page_size: int) -> PaginatedResult:
        total, organizations = await self.organizations_repo.list_by_name(name=name, page_size=page_size, page=page)
        return PaginatedResult(data=organizations, total=total, page=page, page_size=page_size)

    async def search_activity(self,
                              activity_id: int,
                              page: int,
                              page_size: int,
                              all_child: bool = False
                              ) -> PaginatedResult:
        activity_ids = [activity_id]
        if all_child:
            activity_ids = await self.activity_repo.get_activity_ids(activity_id)
        total, organizations = await self.organizations_repo.list_by_activity(activity_ids=activity_ids,
                                                                              page_size=page_size,
                                                                              page=page)
        return PaginatedResult(data=organizations, total=total, page=page, page_size=page_size)

    async def search_building(self, building_id: int, page: int, page_size: int) -> PaginatedResult:
        total, organizations = await self.organizations_repo.list_by_building(building_id=building_id,
                                                                              page_size=page_size,
                                                                              page=page)
        return PaginatedResult(data=organizations, total=total, page=page, page_size=page_size)

    async def get_organization(self, organization_id: int) -> Organization:
        organization = await self.organizations_repo.get_by_id(organization_id)
        return organization

    async def search_organization_within_radius(self,
                                                latitude: float,
                                                longitude: float,
                                                radius: float,
                                                page: int,
                                                page_size: int
                                                ):
        total, organizations = await self.organizations_repo.list_organization_within_radius(
            latitude,
            longitude,
            radius,
            page,
            page_size
        )
        return PaginatedResult(data=organizations, total=total, page=page, page_size=page_size)

    async def search_organization_within_rectangle(self,
                                                   lat_min: float,
                                                   lon_min: float,
                                                   lat_max: float,
                                                   lon_max: float,
                                                   page: int,
                                                   page_size: int
                                                   ):
        total, organizations = await self.organizations_repo.list_organization_within_rectangle(
            lat_min,
            lon_min,
            lat_max,
            lon_max,
            page,
            page_size
        )
        return PaginatedResult(data=organizations, total=total, page=page, page_size=page_size)

