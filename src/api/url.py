from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import RedirectResponse

from src.db.repositories.holder import HolderRepository
from src.di.db import uow_provider
from src.di.url import provide_url_service
from src.di.user import provide_current_user
from src.schemas.url import CreateUrl, UrlSchema, UpdateUrl
from src.schemas.user import UserSchema
from src.services.url import UrlService

router = APIRouter(
    prefix='/url',
    tags=['URLs']
)


@router.get('/{short_url}', response_class=RedirectResponse)
async def get_short_url(
        short_url: str,
        uow: HolderRepository = Depends(uow_provider),
        user: UserSchema = Depends(provide_current_user),
        url_service: UrlService = Depends(provide_url_service)
):
    return await url_service.get_short_url(short_url, user.id, uow)


@router.post('/', response_model=UrlSchema)
async def create_url(
        url_data: CreateUrl,
        uow: HolderRepository = Depends(uow_provider),
        user: UserSchema = Depends(provide_current_user),
        url_service: UrlService = Depends(provide_url_service),
        file: UploadFile = File(...)
):
    return await url_service.create_url(url_data, user.id, file, uow)


@router.get('/user/status', response_model=list[UrlSchema])
async def get_urls(
        uow: HolderRepository = Depends(uow_provider),
        user: UserSchema = Depends(provide_current_user),
        url_service: UrlService = Depends(provide_url_service)
):
    return await url_service.get_urls_by_user(user.id, uow)


@router.patch('/{short_url}', response_model=UrlSchema)
async def update_url(
        short_url: str,
        url_data: UpdateUrl,
        uow: HolderRepository = Depends(uow_provider),
        user: UserSchema = Depends(provide_current_user),
        url_service: UrlService = Depends(provide_url_service)
):
    return await url_service.update_url(url_data, user.id, short_url, uow)
