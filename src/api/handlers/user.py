from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.handlers.requests.user import CreateUser
from src.infrastructure.db.repositories.holder import HolderRepository
from src.api.di.db import uow_provider
from src.api.di.user import get_user_service, provide_current_user
from src.api.handlers.responses.user import Token, UserSchema
from src.usecases.user import UserService

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/sign-up', response_model=Token)
async def sign_up(
        user_data: CreateUser,
        service: UserService = Depends(get_user_service),
        uow: HolderRepository = Depends(uow_provider)
):
    return await service.register_new_user(user_data, user_repo=uow.user_repo, s3_repo=uow.s3_repo)


@router.post('/sign-in', response_model=Token)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: UserService = Depends(get_user_service),
        uow: HolderRepository = Depends(uow_provider)
):
    return await service.authenticate_user(
        form_data.username,
        form_data.password,
        user_repo=uow.user_repo
    )


@router.get('/user', response_model=UserSchema)
async def get_user(user: UserSchema = Depends(provide_current_user)):
    return user
