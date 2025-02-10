from typing import Annotated
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from app.application.services.organization import OrganizationService
from app.containers import Container
from app.interfaces.api.v1.filters.base import BasePaginationParams
from app.interfaces.api.v1.filters.organization import OrganizationFilterByNameParams
from app.interfaces.api.v1.schemas.organization import OrganizationSchema, OrganizationResponseSchema

router = APIRouter()


@router.get("/organization/{organization_id}", response_model=OrganizationSchema)
@inject
async def get_organization_detail(
        organization_id: int,
        organization_services: OrganizationService = Depends(Provide[Container.services.organization_service])
):
    organization = await organization_services.get_organization(organization_id)
    if organization:
        return organization
    raise HTTPException(status_code=404, detail="Organization not found")


@router.get("/organization")
@inject
async def get_organization_by_name(
        params: OrganizationFilterByNameParams = Depends(),
        organization_services: OrganizationService = Depends(Provide[Container.services.organization_service])
):
    organizations = await organization_services.search_organizations(params.name, params.page, params.page_size)

    return OrganizationResponseSchema.model_validate(organizations)


@router.get("/organization/building/{building_id}", response_model=OrganizationResponseSchema)
@inject
async def get_organization_by_building(
        building_id: int,
        params: BasePaginationParams = Depends(),
        organization_services: OrganizationService = Depends(Provide[Container.services.organization_service])
):
    organizations = await organization_services.search_building(building_id, params.page, params.page_size)
    return OrganizationResponseSchema.model_validate(organizations)


@router.get("/organization/activity/{activity_id}", response_model=OrganizationResponseSchema)
@inject
async def get_organization_by_activity(
        activity_id: int,
        params: BasePaginationParams = Depends(),
        organization_services: OrganizationService = Depends(Provide[Container.services.organization_service])
):
    organizations = await organization_services.search_activity(activity_id, params.page, params.page_size)
    return OrganizationResponseSchema.model_validate(organizations)
