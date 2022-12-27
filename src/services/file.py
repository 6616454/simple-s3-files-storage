from asyncio import create_task

import aiofiles
from fastapi import UploadFile

from src.db.repositories.holder import HolderRepository


class FileService:
    async def upload_files(self, user_path: str, dir: str, files: list[UploadFile], uow: HolderRepository):
        for file in files:
            create_task(self.create_file(user_path, dir, file, uow))

    @staticmethod
    async def create_file(user_path: str, dir: str, file: UploadFile, uow: HolderRepository):
        async with aiofiles.open(file.filename, 'wb') as buffer:
            data = await file.read()
            await buffer.write(data)

        if dir is None:
            file_path = f'{buffer.name}'
        else:
            file_path = f'{dir}/{buffer.name}'

        await uow.file_repo.create_file(file_path, dir, buffer.name)
        await uow.s3_repo.upload_file(user_path, file_path, buffer.name)
