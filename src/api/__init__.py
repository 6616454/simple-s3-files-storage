from fastapi import APIRouter

from .url import router as url_router
from .user import router as user_router


def setup_routes(router: APIRouter):
    router.include_router(url_router)
    router.include_router(user_router)
