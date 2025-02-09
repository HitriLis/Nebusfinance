from fastapi import APIRouter
from app.interfaces.api.v1.routers import organization_router

api_router = APIRouter()

# Регистрация маршрутов
api_router.include_router(organization_router, prefix="", tags=["Organization"])
