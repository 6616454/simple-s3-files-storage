from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def create_pool(database_url: str, echo_mode: bool) -> sessionmaker:
    engine = create_async_engine(url=database_url, echo=echo_mode)
    pool = sessionmaker(bind=engine, class_=AsyncSession,
                        expire_on_commit=False, autoflush=False)
    return pool
