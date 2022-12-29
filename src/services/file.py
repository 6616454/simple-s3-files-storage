from asyncio import create_task

import aiofiles
from fastapi import UploadFile

from src.db.models.file import File
from src.db.repositories.holder import HolderRepository
from src.schemas.file import OutputFile


class FileService:
    @staticmethod
    async def create_file(
            user_path: str,
            user_id: int,
            dir: str,
            file: UploadFile,
            uow: HolderRepository
    ):
        async with aiofiles.open(file.filename, 'wb') as buffer:
            data = await file.read()
            await buffer.write(data)

        if dir is None:
            file_path = f'{buffer.name}'
        else:
            file_path = f'{dir}/{buffer.name}'

        await uow.file_repo.create_file(file_path, buffer.name, user_id)
        await uow.s3_repo.upload_file(user_path, file_path, buffer.name)

    async def upload_files(
            self,
            user_path: str,
            user_id: int,
            dir: str,
            files: list[UploadFile],
            uow: HolderRepository
    ):
        for file in files:
            create_task(self.create_file(user_path, user_id, dir, file, uow))

    @staticmethod
    async def get_user_files(user_id: int, uow: HolderRepository) -> list[File]:
        result = await uow.file_repo.get_files_by_user_id(user_id)
        return result
