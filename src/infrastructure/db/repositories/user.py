from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infrastructure.db.models import User
from src.infrastructure.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_user_by_name(self, username: str) -> User:
        query = select(self.model).where(self.model.username == username)
        result = (await self.session.execute(query)).scalar_one_or_none()

        return result

    async def create_user(self, username: str, password_hash: str, user_path: str) -> User:
        user = User(
            username=username,
            password_hash=password_hash,
            user_path=user_path
        )

        await self.save(user)
        await self.refresh(user)

        return user
