from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.building import Building
from ...domain.repositories.building_repository import IBuildingRepository
from ..database.models import Building as BuildingDBModel


class BuildingRepository(IBuildingRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def get_all(self) -> List[Building]:
        db_buildings = self.session.query(BuildingDBModel).all()
        return [
            Building(
                id=b.id,
                address=b.address,
                latitude=b.latitude,
                longitude=b.longitude
            )
            for b in db_buildings
        ]

    def get_by_id(self, building_id: int) -> Building:
        db_building = self.session.query(BuildingDBModel).all()
        return Building(
                id=db_building.id,
                address=db_building.address,
                latitude=db_building.latitude,
                longitude=db_building.longitude
            )
