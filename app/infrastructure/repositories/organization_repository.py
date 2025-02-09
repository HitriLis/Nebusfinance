from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

from ..database.models.organization import organization_activity
from ..database.models import Activity as ActivityModel
from ..database.models import Organization as OrganizationModel

from ...domain.entities.organization import Organization, PhoneNumber
from ...domain.entities.activity import Activity
from ...domain.entities.building import Building
from ...domain.repositories.organization_repository import IOrganizationRepository


class OrganizationRepository(IOrganizationRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

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
            return self.to_dto(model)
        return model

    async def get_by_name(
            self, name: Optional[str] = None, offset: int = 0, limit: int = 10
    ) -> List[Organization]:

        query = select(OrganizationModel).options(
            selectinload(OrganizationModel.phone_numbers),
            selectinload(OrganizationModel.building),
            selectinload(OrganizationModel.activities)
        )

        count_result_query = select(func.count()).select_from(OrganizationModel)
        if name:
            query = query.filter(OrganizationModel.name.ilike(f"%{name}%"))
            count_result_query = count_result_query.filter(OrganizationModel.name.ilike(f"%{name}%"))

        count_result = await self.session.execute(count_result_query)
        total_count = count_result.scalar()

        result = await self.session.execute(
            query.limit(limit).offset(offset)
        )
        organizations = result.scalars().all()
        print(total_count)
        return [self.to_dto(model) for model in organizations]

    async def get_by_activity(self, activity_id: int, offset: int = 0, limit: int = 10) -> List[Organization]:
        cte = (
            select(OrganizationModel.id)
            .join(organization_activity)
            .join(ActivityModel)
            .filter(ActivityModel.id == activity_id)
            .cte('organizations_with_activity')  # CTE для выбора организаций с данным видом деятельности
        )

        result = await self.session.execute(
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities)
            )
            .join(cte, cte.c.id == OrganizationModel.id)  # Присоединение CTE для выборки данных
            .limit(limit)
            .offset(offset)
        )
        organizations = result.scalars().all()

        # Подсчёт общего количества организаций
        count_result = await self.session.execute(
            select(func.count()).select_from(cte)
        )
        total_count = count_result.scalar()
        print(total_count)
        return [self.to_dto(model) for model in organizations]

    async def get_by_building(self, building_id: int, offset: int = 0, limit: int = 10) -> List[Organization]:
        cte = (
            select(OrganizationModel.id)
            .filter(OrganizationModel.building_id == building_id)
            .cte('organizations_in_building')
        )

        # Основной запрос
        result = await self.session.execute(
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities)
            )
            .join(cte, cte.c.id == OrganizationModel.id)  # Присоединяем CTE
            .limit(limit)
            .offset(offset)
        )

        organizations = result.scalars().all()
        count_result = await self.session.execute(
            select(func.count()).select_from(cte)
        )
        total_count = count_result.scalar()
        print(total_count)
        return [self.to_dto(model) for model in organizations]
