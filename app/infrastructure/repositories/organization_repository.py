from typing import Optional, Tuple, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

from ..database.models.organization import organization_activity
from ..database.models import Activity
from ..database.models import Organization
from ...domain.repositories.organization_repository import IOrganizationRepository


class OrganizationRepository(IOrganizationRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _get_pagination_offset(page: int, page_size: int) -> int:
        """
        Проверяет номер страницы и возвращает корректное смещение.
        Если page < 1, то будет установлено значение 1.

        :param page: Номер страницы
        :param page_size: Количество элементов на странице
        :return: Смещение для пагинации
        """
        if page < 1:
            page = 1
        offset = (page - 1) * page_size
        return offset

    async def get_by_id(self, organization_id: int) -> Optional[Organization]:
        result = await self.session.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.building),
                selectinload(Organization.activities)
            )
            .filter(Organization.id == organization_id)
        )
        return result.scalar_one_or_none()

    async def list_by_name(self, name: Optional[str], page: int, page_size: int) -> Tuple[int, Sequence[Organization]]:

        offset = self._get_pagination_offset(page, page_size)
        query = select(Organization).options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.building),
            selectinload(Organization.activities)
        )

        count_result_query = select(func.count()).select_from(Organization)
        if name:
            query = query.filter(Organization.name.ilike(f"%{name}%"))
            count_result_query = count_result_query.filter(Organization.name.ilike(f"%{name}%"))

        count_result = await self.session.execute(count_result_query)
        total_count = count_result.scalar()

        result = await self.session.execute(
            query.limit(page_size).offset(offset)
        )
        return total_count, result.scalars().all()

    async def list_by_activity(self, activity_id: int, page: int, page_size: int) -> Tuple[int, Sequence[Organization]]:
        offset = self._get_pagination_offset(page, page_size)
        cte = (
            select(Organization.id)
            .join(organization_activity)
            .join(Activity)
            .filter(Activity.id == activity_id)
            .cte('organizations_with_activity')
        )

        result = await self.session.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.building),
                selectinload(Organization.activities)
            )
            .join(cte, cte.c.id == Organization.id)
            .limit(page_size)
            .offset(offset)
        )
        organizations = result.scalars().all()
        count_result = await self.session.execute(
            select(func.count()).select_from(cte)
        )
        total_count = count_result.scalar()
        return total_count, organizations

    async def list_by_building(self, building_id: int, page: int, page_size: int) -> Tuple[int, Sequence[Organization]]:
        offset = self._get_pagination_offset(page, page_size)
        cte = (
            select(Organization.id)
            .filter(Organization.building_id == building_id)
            .cte('organizations_in_building')
        )
        result = await self.session.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.building),
                selectinload(Organization.activities)
            )
            .join(cte, cte.c.id == Organization.id)  # Присоединяем CTE
            .limit(page_size)
            .offset(offset)
        )

        organizations = result.scalars().all()
        count_result = await self.session.execute(
            select(func.count()).select_from(cte)
        )
        total_count = count_result.scalar()
        return total_count, organizations
