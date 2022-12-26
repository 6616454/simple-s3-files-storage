from sqlalchemy.orm import sessionmaker

from src.db.repositories.holder import HolderRepository


def uow_provider():
    raise NotImplementedError


class DbProvider:
    def __init__(self, pool: sessionmaker):
        self.pool = pool

    async def provide_session(self):
        async with self.pool() as session:
            yield HolderRepository(session=session)
