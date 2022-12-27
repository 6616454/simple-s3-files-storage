from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.file import File
from src.db.repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):

    def __init__(self, session: AsyncSession):
        super().__init__(File, session)

    async def create_file(self):
        ...
