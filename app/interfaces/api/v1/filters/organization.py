from pydantic import BaseModel, Field

from app.interfaces.api.v1.filters.base import BasePaginationParams


class OrganizationFilterByNameParams(BasePaginationParams):
    name: str = Field(default=None, description="Название компании")

