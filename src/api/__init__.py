from fastapi import APIRouter

from .user import router as user_router
from .file import router as file_router


def setup_routes(router: APIRouter):
    router.include_router(user_router)
    router.include_router(file_router)
