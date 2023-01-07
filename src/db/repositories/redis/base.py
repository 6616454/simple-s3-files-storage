import logging
from typing import Optional

from redis.asyncio import Redis

logger = logging.getLogger('main_logger')


class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis: Redis = redis

    async def set(self, name: str, value: str, ex: Optional[int] = None) -> None:
        logger.info('Redis set - %s:%s', name, value)
        if ex:
            await self.redis.set(name, value, ex=ex)
            return
        await self.redis.set(name, value)

    async def get(self, name: str) -> str:
        result = await self.redis.get(name)
        return result

    async def delete(self, name: str) -> None:
        logger.info('Redis del - %s', name)
        await self.redis.delete(name)
