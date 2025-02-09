from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .building import Building
from .activity import Activity

organization_activity = sa.Table(
    "organization_activity",
    Base.metadata,
    sa.Column("organization_id", sa.ForeignKey("organizations.id"), primary_key=True),
    sa.Column("activity_id", sa.ForeignKey("activities.id"), primary_key=True),
)


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    number: Mapped[str] = mapped_column(sa.String, unique=True)
    organization_id: Mapped[int] = mapped_column(sa.ForeignKey("organizations.id", ondelete='CASCADE'))


class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(sa.ForeignKey("buildings.id"), nullable=True)
    building: Mapped[Building] = relationship(back_populates="organizations")
    activities: Mapped[List[Activity]] = relationship(secondary=organization_activity, backref="organizations")
    phone_numbers: Mapped[List["PhoneNumber"]] = relationship("PhoneNumber", backref="organization",
                                                              cascade="all, delete-orphan")
