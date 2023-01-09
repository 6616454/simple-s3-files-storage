from fastapi import APIRouter

from src.api.handlers.user import router as user_router
from src.api.handlers.file import router as file_router


def setup_routes(router: APIRouter):
    router.include_router(user_router)
    router.include_router(file_router)
