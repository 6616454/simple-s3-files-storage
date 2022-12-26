from sqlalchemy.orm import sessionmaker
from redis.asyncio import Redis

from src.db.repositories.holder import HolderRepository


def uow_provider():
    raise NotImplementedError


class DbProvider:
    def __init__(self, pool: sessionmaker, redis: Redis):
        self.pool = pool
        self.redis = redis

    async def provide_session(self):
        async with self.pool() as session:
            yield HolderRepository(session=session, redis=self.redis)
