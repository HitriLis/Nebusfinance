from typing import List
from sqlalchemy import select, func, literal_column
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.building import Building
from ...domain.repositories.activity_repository import IActivityRepository
from ..database.models import Activity


class ActivityRepository(IActivityRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_activity_ids(self, activity_id: int) -> List[int]:
        activity_alias = aliased(Activity)
        cte = (
            select(Activity)
            .where(Activity.id == activity_id)
            .cte(recursive=True)
        )

        cte = cte.union_all(
            select(activity_alias)
            .where(activity_alias.parent_id == cte.c.id)
        )
        cte_query = select(cte)
        result = await self.session.execute(cte_query)
        all_activities = result.scalars().all()
        return all_activities
