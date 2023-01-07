from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.file import File
from src.db.repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):

    def __init__(self, session: AsyncSession):
        super().__init__(File, session)

    async def create_file(self, file_path: str, file_name: str, user_id: int) -> None:
        file_obj = self.model(
            file_name=file_name,
            file_path=file_path,
            user_id=user_id
        )

        await self.save(file_obj)
        await self.commit()
        await self.refresh(file_obj)

        return file_obj

    async def get_files_by_user_id(self, user_id: int) -> list[File]:
        query = select(self.model).where(self.model.user_id == user_id)
        result = (await self.session.execute(query)).scalars().all()
        return result

    async def get_file_by_user_and_id(self, file_id: int, user_id: int) -> File:
        query = select(self.model).where(and_(self.model.user_id == user_id, self.model.id == file_id))
        result = (await self.session.execute(query)).scalar_one_or_none()
        return result
