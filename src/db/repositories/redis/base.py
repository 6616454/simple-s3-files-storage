from redis.asyncio import Redis


class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis
