from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ...domain.entities.organization import Organization, PhoneNumber
from ...domain.entities.activity import Activity
from ...domain.entities.building import Building
from ...domain.repositories.organization_repository import IOrganizationRepository
from ..database.models import Organization as OrganizationModel


class OrganizationRepository(IOrganizationRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, organization_id: int) -> Optional[Organization]:
        result = await self.session.execute(
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities)
            )
            .filter(OrganizationModel.id == organization_id)
        )
        model = result.scalar_one_or_none()
        if model:
            phone_numbers = [  # Конвертация phone_numbers
                PhoneNumber(id=p.id, number=p.number) for p in model.phone_numbers
            ]
            activities = [  # Конвертация activities
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
        return None

    async def get_all(self) -> List[Organization]:
        pass

    async def get_by_activity(self, activity_id: int) -> List[Organization]:
        pass
