from typing import Optional, Tuple, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from geoalchemy2 import WKTElement
from geoalchemy2.functions import ST_Transform, ST_DWithin
from geoalchemy2.shape import to_shape

from ..database.models.organization import organization_activity
from ..database.models import Activity as ActivityModel
from ..database.models import Organization as OrganizationModel
from ..database.models import Building as BuildModel
from ...domain.repositories.organization_repository import IOrganizationRepository

from ...domain.entities.organization import Organization, PhoneNumber
from ...domain.entities.activity import Activity
from ...domain.entities.building import Building


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
            latitude=to_shape(model.building.geom).y,
            longitude=to_shape(model.building.geom).x
        )
        return Organization(
            id=model.id,
            name=model.name,
            building=building,
            phone_numbers=phone_numbers,
            activities=activities,
        )

    @staticmethod
    def _get_pagination_offset(page: int, page_size: int) -> int:
        if page < 1:
            page = 1
        offset = (page - 1) * page_size
        return offset

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
        organization = result.scalar_one_or_none()
        if organization:
            return self.to_dto(organization)
        return None

    async def list_by_name(self, name: Optional[str], page: int, page_size: int) -> Tuple[int, List[Organization]]:

        offset = self._get_pagination_offset(page, page_size)
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
            query.limit(page_size).offset(offset)
        )
        organizations = result.scalars().all()
        return total_count, [self.to_dto(item) for item in organizations]

    async def list_by_activity(self, activity_ids: List[int], page: int, page_size: int) -> Tuple[int, List[Organization]]:
        offset = self._get_pagination_offset(page, page_size)
        cte = (
            select(OrganizationModel.id)
            .join(organization_activity)
            .join(OrganizationModel)
            .filter(ActivityModel.id.in_(activity_ids))
            .cte('organizations_with_activity')
        )

        result = await self.session.execute(
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities)
            )
            .join(cte, cte.c.id == OrganizationModel.id)
            .limit(page_size)
            .offset(offset)
        )
        organizations = result.scalars().all()
        count_result = await self.session.execute(
            select(func.count()).select_from(cte)
        )
        total_count = count_result.scalar()
        return total_count, [self.to_dto(item) for item in organizations]

    async def list_by_building(self, building_id: int, page: int, page_size: int) -> Tuple[int, List[Organization]]:
        offset = self._get_pagination_offset(page, page_size)
        cte = (
            select(OrganizationModel.id)
            .filter(OrganizationModel.building_id == building_id)
            .cte('organizations_in_building')
        )
        result = await self.session.execute(
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities)
            )
            .join(cte, cte.c.id == OrganizationModel.id)
            .limit(page_size)
            .offset(offset)
        )

        organizations = result.scalars().all()
        count_result = await self.session.execute(
            select(func.count()).select_from(cte)
        )
        total_count = count_result.scalar()
        return total_count, [self.to_dto(item) for item in organizations]

    async def list_organization_within_radius(self,
                                              latitude: float,
                                              longitude: float,
                                              radius: float,
                                              page: int,
                                              page_size: int
                                              ) -> Tuple[int, List[Organization]]:

        offset = self._get_pagination_offset(page, page_size)

        point = WKTElement(f"POINT({longitude} {latitude})", srid=4326)
        point_transformed = ST_Transform(point, 3857)

        cte = (
            select(OrganizationModel.id)
            .join(OrganizationModel.building)
            .filter(ST_DWithin(ST_Transform(BuildModel.geom, 3857), point_transformed, radius * 1000))
            .cte('organizations_in_radius')
        )
        result = await self.session.execute(
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities)
            )
            .join(cte, cte.c.id == OrganizationModel.id)
            .limit(page_size)
            .offset(offset)
        )

        organizations = result.scalars().all()

        count_result = await self.session.execute(
            select(func.count()).select_from(cte)
        )
        total_count = count_result.scalar()

        return total_count, [self.to_dto(item) for item in organizations]

    async def list_organization_within_rectangle(self,
                                                 lat_min: float,
                                                 lon_min: float,
                                                 lat_max: float,
                                                 lon_max: float,
                                                 page: int,
                                                 page_size: int
                                                 ) -> Tuple[int, List[Organization]]:
        offset = self._get_pagination_offset(page, page_size)
        polygon_wkt = f"POLYGON(({lon_min} {lat_min}, {lon_min} {lat_max}, {lon_max} {lat_max}, {lon_max} {lat_min}, {lon_min} {lat_min}))"
        polygon = WKTElement(polygon_wkt, srid=4326)

        cte = (
            select(OrganizationModel.id)
            .join(OrganizationModel.building)
            .filter(ST_DWithin(BuildModel.geom, polygon))
            .cte('organizations_in_radius')
        )
        result = await self.session.execute(
            select(OrganizationModel)
            .options(
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.building),
                selectinload(OrganizationModel.activities)
            )
            .join(cte, cte.c.id == OrganizationModel.id)
            .limit(page_size)
            .offset(offset)
        )

        organizations = result.scalars().all()

        count_result = await self.session.execute(
            select(func.count()).select_from(cte)
        )
        total_count = count_result.scalar()

        return total_count, [self.to_dto(item) for item in organizations]
