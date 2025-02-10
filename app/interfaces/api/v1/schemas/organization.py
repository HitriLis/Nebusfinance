from typing import Optional, List
from pydantic import BaseModel
from app.interfaces.api.v1.schemas.building import BuildingSchema


class ActivitySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PhoneNumberSchema(BaseModel):
    id: int
    number: str

    class Config:
        from_attributes = True


class OrganizationSchema(BaseModel):
    id: int
    name: str
    building: BuildingSchema
    phone_numbers: List[PhoneNumberSchema]
    activities: List[ActivitySchema]

    class Config:
        from_attributes = True


class OrganizationResponseSchema(BaseModel):
    total: int
    page: int
    total_pages: int
    next_page: Optional[int]
    prev_page: Optional[int]
    data: List[OrganizationSchema]

    class Config:
        from_attributes = True
