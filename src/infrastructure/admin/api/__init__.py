from fastapi import FastAPI, APIRouter

from .list import router as list_router
from .info import router as info_router


def register_routers(app: FastAPI) -> None:
    api_router = APIRouter(prefix="/api")

    api_router.include_router(list_router, prefix="/list")
    api_router.include_router(info_router, prefix="/info")

    app.include_router(api_router)
