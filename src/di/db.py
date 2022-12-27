from aioboto3 import Session
from sqlalchemy.orm import sessionmaker
from redis.asyncio import Redis

from src.core.config import Settings
from src.db.repositories.holder import HolderRepository


def uow_provider():
    raise NotImplementedError


class DbProvider:
    def __init__(self, pool: sessionmaker, redis: Redis, s3_session: Session, settings: Settings):
        self.pool = pool
        self.redis = redis
        self.s3_session = s3_session
        self.settings = settings

    async def provide_session(self):
        async with self.pool() as session:
            yield HolderRepository(
                session=session,
                redis=self.redis,
                s3_session=self.s3_session,
                settings=self.settings
            )
