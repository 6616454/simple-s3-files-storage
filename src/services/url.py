import logging

import shortuuid
from fastapi import HTTPException

from fastapi.responses import RedirectResponse
from fastapi import status
from sqlalchemy.exc import ProgrammingError
from starlette.responses import JSONResponse

from src.db.repositories.holder import HolderRepository
from src.dto.url import UpdateUrl, CreateUrl, UrlDTO

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
    async def get_urls_by_user(user_id: int, uow: HolderRepository) -> list[UrlDTO]:
        return await uow.url_repo.get_urls_by_user_id(user_id)

    @staticmethod
    async def update_url(url_data: UpdateUrl, user_id: int, short_url: str, uow: HolderRepository) -> UrlDTO:
        new_data = url_data.dict(exclude_unset=True)
        try:
            await uow.url_repo.update_url(short_url=short_url, user_id=user_id, **new_data)
        except ProgrammingError:
            logger.warning('Invalid update operation')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Empty body request')

        new_url = await uow.url_repo.get_url_by_short(short_url, user_id)
        return new_url.to_url_schema()

    async def create_url(self, url_data: CreateUrl, user_id: int, uow: HolderRepository) -> UrlDTO:

        logger.info('Create new URL %s', url_data.original_url)

        return await uow.url_repo.create_url(
            original_url=url_data.original_url,
            short_url=await self.create_short_url(),
            public=url_data.public,
            visibility=url_data.visibility,
            user_id=user_id
        )
