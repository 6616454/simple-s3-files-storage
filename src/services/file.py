import json
import shutil
from typing import Optional
import aiofiles
import os as sync_os
from aiofiles import os
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette import status

from src.infrastructure.db.models import File
from src.infrastructure.db.repositories.file import FileRepository
from src.infrastructure.db.repositories.redis import RedisRepository
from src.infrastructure.db.repositories.s3 import S3Repository


class FileService:
    _file_path: Optional[str]
    _bytes_for_read: int = 1048576  # 1 mb
    _max_bytes: int = 1048576000  # 1 GB

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
    async def get_user_files(
        user_id: int,
        file_repo: FileRepository,
        redis_repo: RedisRepository
    ) -> list[File]:
        cache = await redis_repo.get(user_id)
        if cache:
            return json.loads(cache)

        result = await file_repo.get_files_by_user_id(user_id)
        await redis_repo.set(user_id, json.dumps(
            [file.to_file_schema().dict() for file in result]))

        return result

    async def _create_file(
        self,
        user_path: str,
        user_id: int,
        file_path: str,
        file: UploadFile,
        file_obj: File,
        file_repo: FileRepository,
        s3_repo: S3Repository,
        redis_repo: RedisRepository
    ) -> None:
        _bytes = 0

        async with aiofiles.open(file.filename, 'wb') as buffer:
            data = await file.read(size=self._bytes_for_read)
            await buffer.write(data)
            _bytes += self._bytes_for_read
            await file.seek(offset=_bytes)

            while data:
                try:
                    data = await file.read(size=self._bytes_for_read)
                    await buffer.write(data)
                    _bytes += self._bytes_for_read
                    await file.seek(offset=_bytes)
                except ValueError:
                    break
                if _bytes > self._max_bytes:
                    await file_repo.delete(file_obj)
                    await os.remove(file.filename)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='The file exceeds 1 GB.'
                    )

                await buffer.write(data)

        await s3_repo.upload_file(user_path, file_path, buffer.name)
        await file_repo.update_obj(file_obj.id, downloadable=True)
        await redis_repo.delete(user_id)

        await os.remove(file.filename)

    async def _download_dir(
        self,
        user_path: str,
        dir: str,
        s3_repo: S3Repository
    ) -> FileResponse:
        await s3_repo.get_bucket_by_dir(user_path, dir)

        try:
            shutil.make_archive(dir, 'zip', dir)
            shutil.rmtree(dir)
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Directory not found')

        return await self._file_response(f'{dir}.zip', dir)

    async def upload_files(
        self,
        user_path: str,
        user_id: int,
        dir: str,
        files: list[UploadFile],
        file_repo: FileRepository,
        s3_repo: S3Repository,
        redis_repo: RedisRepository
    ) -> list[File]:

        new_files = []

        if dir is None:
            self._file_path = ''
        else:
            self._file_path = f'{dir}/'

        for file in files:
            file_path = sync_os.path.join(self._file_path + file.filename)

            new_file = await file_repo.create_file(file_path, file.filename, user_id)
            new_files.append(new_file)

            await self._create_file(
                user_path,
                user_id,
                file_path,
                file,
                new_file,
                file_repo,
                s3_repo,
                redis_repo
            )

        await redis_repo.delete(user_id)

        return new_files

    async def download_files(
        self,
        dir: Optional[str],
        file_id: Optional[int],
        user_id: int,
        user_path: str,
        compr_type: Optional[str],
        file_repo: FileRepository,
        s3_repo: S3Repository
    ) -> FileResponse:

        if dir:
            return await self._download_dir(user_path, dir, s3_repo)

        file: File = await file_repo.get_file_by_user_and_id(file_id, user_id)

        if file and file.downloadable:
            await s3_repo.download_file(user_path, file.file_name, file.file_path)
            file_path = await self._compr_type(file.file_name, compr_type)
            return await self._file_response(file_path, file.file_name)

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found.')
