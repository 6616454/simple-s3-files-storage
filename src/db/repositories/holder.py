from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.user import UserRepository


class HolderRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(self.session)
