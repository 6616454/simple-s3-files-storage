from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.file import File
from src.db.repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):

    def __init__(self, session: AsyncSession):
        super().__init__(File, session)

    async def create_file(self, file_path: str, file_name: str, user_id: int):
        file_obj = self.model(
            file_name=file_name,
            file_path=file_path,
            user_id=user_id
        )

        await self.save(file_obj)
        await self.session.flush()
        await self.commit()
