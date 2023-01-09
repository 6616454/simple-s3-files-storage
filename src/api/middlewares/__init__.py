from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .blacklist import BlackListMiddleware
from src.core.config import Settings


def setup_middlewares(app: FastAPI, settings: Settings) -> None:
    black_list = BlackListMiddleware(settings.black_list)

    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=black_list)
