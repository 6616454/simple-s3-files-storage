from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.db.repositories.redis.base import RedisRepository
from src.db.repositories.user import UserRepository


class HolderRepository:

    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.user_repo = UserRepository(self.session)
        self.redis_repo = RedisRepository(redis)

    async def commit(self):
        await self.session.commit()
