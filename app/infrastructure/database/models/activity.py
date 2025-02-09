from typing import List, TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Activity(Base):
    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=True)
    parent_id: Mapped[int] = mapped_column(sa.ForeignKey("activities.id"), nullable=True)
    sub_activities: Mapped[List["Activity"]] = relationship(backref="parent", remote_side=[id])
