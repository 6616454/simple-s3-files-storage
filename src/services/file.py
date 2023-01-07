import json
import shutil
from asyncio import create_task
from typing import Optional, Union
import aiofiles
from aiofiles import os
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette import status

from src.db.models.file import File
from src.db.repositories.holder import HolderRepository


class FileService:
    file_path: Optional[str]

    @staticmethod
    async def _compr_type(file_name: str, _type: Optional[str] = None):
        if _type:
            shutil.make_archive(file_name, _type, file_name)
            await os.remove(file_name)
            return f'{file_name}.{_type}'

        return file_name

    @staticmethod
    async def _file_response(file_path: str, file_name: str) -> FileResponse:
        return FileResponse(
            path=file_path,
            filename=file_name

        )

    @staticmethod
    async def get_user_files(user_id: int, uow: HolderRepository) -> list[File]:
        cache = await uow.redis_repo.get(user_id)
        if cache:
            return json.loads(cache)

        result = await uow.file_repo.get_files_by_user_id(user_id)
        await uow.redis_repo.set(user_id, json.dumps([file.to_file_schema().dict() for file in result]))

        return result

    @staticmethod
    async def _create_file(
            user_path: str,
            user_id: int,
            file_path: str,
            file: UploadFile,
            file_id: int,
            uow: HolderRepository
    ) -> None:
        async with aiofiles.open(file.filename, 'wb') as buffer:
            data = await file.read()
            await buffer.write(data)

        await uow.s3_repo.upload_file(user_path, file_path, buffer.name)
        await uow.file_repo.update_obj(file_id, downloadable=True)
        await uow.redis_repo.delete(user_id)

        await os.remove(file.filename)

    async def _download_dir(self, user_path: str, dir: str, uow: HolderRepository) -> FileResponse:
        await uow.s3_repo.get_bucket_by_dir(user_path, dir)

        try:
            shutil.make_archive(dir, 'zip', dir)
            shutil.rmtree(dir)
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Directory not found')

        return await self._file_response(f'{dir}.zip', dir)

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

            create_task(self._create_file(user_path, user_id, file_path, file, new_file.id, uow))

        await uow.redis_repo.delete(user_id)

        return new_files

    async def download_files(
            self,
            dir: Optional[str],
            file_id: Optional[int],
            user_id: int,
            user_path: str,
            compr_type: Optional[str],
            uow: HolderRepository
    ) -> FileResponse:

        if dir:
            return await self._download_dir(user_path, dir, uow)

        file: File = await uow.file_repo.get_file_by_user_and_id(file_id, user_id)

        if file and file.downloadable:
            await uow.s3_repo.download_file(user_path, file.file_name, file.file_path)
            file_path = await self._compr_type(file.file_name, compr_type)
            return await self._file_response(file_path, file.file_name)

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found.')
