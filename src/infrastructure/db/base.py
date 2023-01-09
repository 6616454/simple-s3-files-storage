import logging

import aioboto3
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from redis.asyncio import Redis

logger = logging.getLogger('main_logger')

Base = declarative_base()


def create_pool(database_url: str, echo_mode: bool) -> sessionmaker:
    engine = create_async_engine(url=database_url, echo=echo_mode)
    pool = sessionmaker(bind=engine, class_=AsyncSession,
                        expire_on_commit=False, autoflush=False)
    return pool


def create_redis(redis_host: str, redis_port: int, redis_db: int) -> Redis:
    logger.info('Creating Redis...')
    return Redis(host=redis_host, port=redis_port, db=redis_db)


def create_s3():
    session = aioboto3.Session()
    return session
