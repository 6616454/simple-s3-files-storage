from asyncio import create_task
from typing import Optional

import aiofiles
from aiofiles import os
from fastapi import UploadFile

from src.db.models.file import File
from src.db.repositories.holder import HolderRepository


class FileService:
    file_path: Optional[str]

    @staticmethod
    async def get_user_files(user_id: int, uow: HolderRepository) -> list[File]:
        result = await uow.file_repo.get_files_by_user_id(user_id)
        return result

    @staticmethod
    async def create_file(
            user_path: str,
            file_path: str,
            file: UploadFile,
            file_id: int,
            uow: HolderRepository
    ):
        async with aiofiles.open(file.filename, 'wb') as buffer:
            data = await file.read()
            await buffer.write(data)

        await uow.s3_repo.upload_file(user_path, file_path, buffer.name)
        await uow.file_repo.update_obj(file_id, downloadable=True)
        await os.remove(file.filename)

    async def upload_files(
            self,
            user_path: str,
            user_id: int,
            dir: str,
            files: list[UploadFile],
            uow: HolderRepository
    ) -> list[File]:

        new_files = []

        if dir is None:
            self.file_path = ''
        else:
            self.file_path = f'{dir}/'

        for file in files:
            file_path = self.file_path + file.filename

            new_file = await uow.file_repo.create_file(file_path, file.filename, user_id)
            new_files.append(new_file)

            create_task(self.create_file(user_path, file_path, file, new_file.id, uow))

        return new_files
