from aiofiles import os
import os as sync_os

from aioboto3 import Session
from aiobotocore.config import AioConfig


class S3Repository:
    def __init__(self, session: Session, s3_host: str, user: str, password: str):
        self.session = session
        self.s3_host = s3_host
        self.user = user
        self.password = password

    async def get_bucket_by_dir(self, user_path: str, dir: str) -> None:
        async with self.session.resource(
            's3',
            endpoint_url=self.s3_host,
            aws_access_key_id=self.user,
            aws_secret_access_key=self.password,
            config=AioConfig(signature_version='s3v4')
        ) as s3:
            bucket = await s3.Bucket(user_path)
            async for s3_object in bucket.objects.filter(Prefix=dir):
                path, filename = sync_os.path.split(s3_object.key)
                await os.makedirs(path, exist_ok=True)
                await bucket.download_file(s3_object.key, sync_os.path.join(path, filename))

    async def upload_file(self, user_path: str, file_path: str, file: str) -> None:
        async with self.session.resource(
            's3',
            endpoint_url=self.s3_host,
            aws_access_key_id=self.user,
            aws_secret_access_key=self.password,
            config=AioConfig(signature_version='s3v4')
        ) as s3:
            bucket = await s3.Bucket(user_path)
            await bucket.upload_file(file, file_path)

    async def create_bucket(self, user_path: str):
        async with self.session.resource(
            's3',
            endpoint_url=self.s3_host,
            aws_access_key_id=self.user,
            aws_secret_access_key=self.password,
            config=AioConfig(signature_version='s3v4')
        ) as s3:
            await s3.create_bucket(Bucket=user_path)

    async def download_file(self, user_path: str, file_name: str, file_path: str) -> None:
        async with self.session.resource(
            's3',
            endpoint_url=self.s3_host,
            aws_access_key_id=self.user,
            aws_secret_access_key=self.password,
            config=AioConfig(signature_version='s3v4')
        ) as s3:
            bucket = await s3.Bucket(user_path)
            await bucket.download_file(file_path, file_name)

    async def delete_bucket(self, user_path: str):
        async with self.session.resource(
            's3',
            endpoint_url=self.s3_host,
            aws_access_key_id=self.user,
            aws_secret_access_key=self.password,
            config=AioConfig(signature_version='s3v4')
        ) as s3:
            bucket = await s3.Bucket(user_path)
            await bucket.delete()
