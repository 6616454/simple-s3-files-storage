from aioboto3 import Session
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from redis.asyncio import Redis

from src.core.config import Settings
from src.di.db import DbProvider, uow_provider
from src.di.user import get_user_service, provide_current_user
from src.di.file import provide_file_service
from src.services.file import FileService
from src.services.user import UserService


def setup_dependency_injection(app: FastAPI, pool: sessionmaker, redis: Redis, s3_session: Session, settings: Settings):
    db_provider = DbProvider(pool=pool, redis=redis, s3_session=s3_session, settings=settings)
    user_service = UserService(
        settings.jwt_expiration,
        settings.jwt_secret,
        settings.jwt_algorithm
    )

    file_service = FileService()

    app.dependency_overrides[uow_provider] = db_provider.provide_session
    app.dependency_overrides[get_user_service] = lambda: user_service
    app.dependency_overrides[provide_current_user] = user_service.get_current_user
    app.dependency_overrides[provide_file_service] = lambda: file_service
