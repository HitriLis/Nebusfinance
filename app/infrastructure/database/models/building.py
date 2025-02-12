from typing import List, TYPE_CHECKING
import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .organization import Organization


class Building(Base):
    __tablename__ = "buildings"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    address: Mapped[str] = mapped_column(sa.String, nullable=True, index=True)
    geom: Mapped[str] = mapped_column(Geometry("POINT", srid=4326))
    organizations: Mapped[List["Organization"]] = relationship(back_populates="building")
