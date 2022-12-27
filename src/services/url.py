import logging

import shortuuid
from fastapi import HTTPException, UploadFile

from fastapi.responses import RedirectResponse
from fastapi import status
from sqlalchemy.exc import ProgrammingError

from src.db.repositories.holder import HolderRepository
from src.schemas.url import UpdateUrl, CreateUrl, UrlSchema

logger = logging.getLogger('main_logger')


class UrlService:

    @staticmethod
    async def create_short_url() -> shortuuid.ShortUUID:
        return shortuuid.uuid()

    @staticmethod
    async def get_short_url(short_url: str, user_id: int, uow: HolderRepository) -> RedirectResponse:
        url = await uow.url_repo.get_url_by_short(short_url=short_url)

        if url:
            url.counter += 1
            await uow.url_repo.commit()

        if url.public or url.user_id == user_id:
            return RedirectResponse(url.original_url)

        logger.warning('User try to get undefined short url - %s', short_url)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ShortUrl Not Found')

    @staticmethod
    async def get_urls_by_user(user_id: int, uow: HolderRepository) -> list[UrlSchema]:
        return await uow.url_repo.get_urls_by_user_id(user_id)

    @staticmethod
    async def update_url(url_data: UpdateUrl, user_id: int, short_url: str, uow: HolderRepository) -> UrlSchema:
        new_data = url_data.dict(exclude_unset=True)
        try:
            await uow.url_repo.update_url(short_url=short_url, user_id=user_id, **new_data)
        except ProgrammingError:
            logger.warning('Invalid update operation')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Empty body request')

        new_url = await uow.url_repo.get_url_by_short(short_url, user_id)
        return new_url

    async def create_url(self, url_data: CreateUrl, user_id: int, file: UploadFile, uow: HolderRepository) -> UrlSchema:

        logger.info('Create new URL for file - %s', file.filename)
        file = await uow.file_repo.create_file()

        return await uow.url_repo.create_url(
            short_url=await self.create_short_url(),
            public=url_data.public,
            visibility=url_data.visibility,
            user_id=user_id
        )
