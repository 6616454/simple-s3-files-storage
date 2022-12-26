from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from src.core.config import Settings
from src.di.db import DbProvider, uow_provider
from src.di.user import get_user_service, provide_current_user
from src.services.user import UserService


def setup_dependency_injection(app: FastAPI, pool: sessionmaker, settings: Settings):
    db_provider = DbProvider(pool=pool)
    user_service = UserService(
        settings
    )

    app.dependency_overrides[uow_provider] = db_provider.provide_session
    app.dependency_overrides[get_user_service] = lambda: user_service
    app.dependency_overrides[provide_current_user] = user_service.get_current_user
