from aioboto3 import Session
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.core.config import Settings
from src.infrastructure.db.repositories.file import FileRepository
from src.infrastructure.db.repositories.redis import RedisRepository
from src.infrastructure.db.repositories.s3 import S3Repository
from src.infrastructure.db.repositories.user import UserRepository


class HolderRepository:

    def __init__(self, session: AsyncSession, redis: Redis, s3_session: Session, settings: Settings):
        self.session = session
        self.user_repo = UserRepository(self.session)
        self.file_repo = FileRepository(self.session)
        self.redis_repo = RedisRepository(redis)
        self.s3_repo = S3Repository(
            s3_session,
            settings.s3_host,
            settings.minio_root_user,
            settings.minio_root_password
        )

    async def commit(self):
        await self.session.commit()
