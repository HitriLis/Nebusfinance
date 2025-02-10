from typing import Optional
from app.infrastructure.database.models import Organization as OrganizationModel
from ...domain.entities.organization import Organization, PhoneNumber
from ...domain.entities.activity import Activity
from ...domain.entities.building import Building
from ...domain.entities.paginated_result import PaginatedResult
from ...domain.repositories.organization_repository import IOrganizationRepository


class OrganizationService:
    def __init__(self, repository: IOrganizationRepository):
        self.repository = repository

    async def search_organizations(self, name: Optional[str], page: int, page_size: int):
        total, organizations = await self.repository.list_by_name(name=name, page_size=page_size, page=page)
        return PaginatedResult(data=organizations, total=total, page=page, page_size=page_size)

    async def search_activity(self, activity_id: int, page: int, page_size: int):
        total, organizations = await self.repository.list_by_activity(activity_id=activity_id, page_size=page_size,
                                                                      page=page)
        return PaginatedResult(data=organizations, total=total, page=page, page_size=page_size)

    async def search_building(self, building_id: int, page: int, page_size: int) -> PaginatedResult:
        total, organizations = await self.repository.list_by_building(building_id=building_id, page_size=page_size,
                                                                      page=page)
        return PaginatedResult(data=organizations, total=total, page=page, page_size=page_size)

    async def get_organization(self, organization_id: int):
        organization = await self.repository.get_by_id(organization_id)
        return self.to_dto(organization)

    @staticmethod
    def to_dto(model: OrganizationModel) -> Organization:
        phone_numbers = [
            PhoneNumber(id=p.id, number=p.number) for p in model.phone_numbers
        ]
        activities = [
            Activity(id=a.id, name=a.name) for a in model.activities
        ]
        building = Building(
            id=model.building.id,
            address=model.building.address,
            latitude=model.building.latitude,
            longitude=model.building.longitude
        )
        return Organization(
            id=model.id,
            name=model.name,
            building=building,
            phone_numbers=phone_numbers,
            activities=activities,
        )
