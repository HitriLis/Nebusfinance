from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.infrastructure.repositories.organization_repository import OrganizationRepository
from app.containers import Container
from app.interfaces.api.v1.schemas.organization import OrganizationSchema, OrganizationResultSchema

router = APIRouter()


@router.get("/organization/{organization_id}", response_model=OrganizationSchema)
@inject
async def get_organization_detail(
        organization_id: int,
        organization_repository: OrganizationRepository = Depends(Provide[Container.repository.organization_repository])
):
    organization = await organization_repository.get_by_id(organization_id)

    if organization:
        return OrganizationSchema.model_validate(organization)
    raise HTTPException(status_code=404, detail='e')


@router.get("/organization/", response_model=OrganizationResultSchema)
@inject
async def get_organization_by_name(
        name: str,
        organization_repository: OrganizationRepository = Depends(Provide[Container.repository.organization_repository])
):
    organizations = await organization_repository.get_by_name(name)

    return OrganizationResultSchema(data=organizations)


@router.get("/organization/building/{building_id}", response_model=OrganizationResultSchema)
@inject
async def get_organization_by_building(
        building_id: int,
        organization_repository: OrganizationRepository = Depends(Provide[Container.repository.organization_repository])
):
    organizations = await organization_repository.get_by_building(building_id)
    return OrganizationResultSchema(data=organizations)


@router.get("/organization/activity/{activity_id}", response_model=OrganizationResultSchema)
@inject
async def get_organization_by_activity(
        activity_id: int,
        organization_repository: OrganizationRepository = Depends(Provide[Container.repository.organization_repository])
):
    organizations = await organization_repository.get_by_activity(activity_id)
    return OrganizationResultSchema(data=organizations)
