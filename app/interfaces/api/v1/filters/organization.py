from pydantic import BaseModel, Field

from app.interfaces.api.v1.filters.base import BasePaginationParams


class OrganizationFilterByNameParams(BasePaginationParams):
    name: str = Field(default=None, description="Название компании")


class OrganizationFilterByActivityParams(BasePaginationParams):
    all_child: bool = Field(default=False, description="Вложенные виды деятельности")


class OrganizationFilterByRadiusParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Широта точки поиска (-90 до 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота точки поиска (-180 до 180)")
    radius: int = Field(..., gt=0, description="Радиус поиска в километрах")


class OrganizationFilterRectangleParams(BaseModel):
    lat_min: float = Field(..., ge=-90, le=90, description="Минимальная широта прямоугольной области (-90 до 90)")
    lon_min: float = Field(..., ge=-180, le=180, description="Минимальная долгота прямоугольной области (-180 до 180)")
    lat_max: float = Field(..., ge=-90, le=90, description="Максимальная широта прямоугольной области (-90 до 90)")
    lon_max: float = Field(..., ge=-180, le=180, description="Максимальная долгота прямоугольной области (-180 до 180)")
