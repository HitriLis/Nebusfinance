from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.containers import Container
security = HTTPBearer()


# @inject
# def get_current_user(
#         request: Request,
#         credentials: HTTPAuthorizationCredentials = Depends(security),
#         auth_service: AuthService = Depends(Provide[Container.auth_service]),
# ) -> Request:
#     token = credentials.credentials
#     try:
#         payload = auth_service.decode_token(token)
#         payload.pop('exp')
#         request.state.user = AuthUser(**payload)  # Добавляем данные пользователя в state
#         return request
#     except ValueError as e:
#         raise HTTPException(status_code=401, detail=str(e))
