from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.containers import Container
from app.interfaces.api.v1 import api_router
# Создаем приложение
app = FastAPI(
    title="FastAPI Application",
    description="API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Укажите конкретные домены для production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

container = Container()
container.wire(modules=[
    "app.interfaces.api.v1.routers.organization",
    "app.infrastructure.cli.fixture",
])
app.include_router(api_router, prefix="/api/v1")
