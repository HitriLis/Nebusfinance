from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.infrastructure.repositories.organization_repository import OrganizationRepository
from app.containers import Container
from app.interfaces.api.v1.schemas.organization import OrganizationSchema

router = APIRouter()


@router.get("/organization/{organization_id}", response_model=OrganizationSchema)
@inject
async def get_organization(
        organization_id: int,
        organization_repository: OrganizationRepository = Depends(Provide[Container.repository.organization_repository])
):
    organization = await organization_repository.get_by_id(organization_id)

    if organization:
        return OrganizationSchema.model_validate(organization)
    raise HTTPException(status_code=404, detail=str('e'))

# @router.post("/refresh", response_model=TokenResponseSchema)
# @inject
# async def get_refresh_token(
#         data: RefreshTokenSchema,
#         auth_service: AuthService = Depends(Provide[Container.auth_service]),
#         user_repository: SQLAlchemyUserRepository = Depends(Provide[Container.repository.user_repository])
# ):
#     # Проверяем refresh token
#     try:
#         decoded = auth_service.decode_token(data.refresh_token)
#         chat_id = decoded.get("chat_id")
#         user = await user_repository.get_by_chat_id(chat_id)
#         if not user:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
#
#         access_token = auth_service.create_access_token(user)
#         refresh_token = auth_service.create_refresh_token(user)
#         return {"access_token": access_token, "refresh_token": refresh_token}
#     except ValueError as e:
#         raise HTTPException(status_code=401, detail=str(e))
