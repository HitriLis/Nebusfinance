from pydantic import BaseModel, Field


class BasePaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Номер страницы (минимум 1)")
    page_size: int = Field(10, ge=1, le=100, description="Размер страницы (от 1 до 100)")
