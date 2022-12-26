from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.db.repositories.holder import HolderRepository
from src.di.db import uow_provider
from src.di.user import get_user_service, provide_current_user
from src.dto.user import Token, CreateUser, UserDTO
from src.services.user import UserService

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
    return await service.register_new_user(user_data, uow=uow)


@router.post('/sign-in', response_model=Token)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: UserService = Depends(get_user_service),
        uow: HolderRepository = Depends(uow_provider)
):
    return await service.authenticate_user(
        form_data.username,
        form_data.password,
        uow=uow
    )


@router.get('/user', response_model=UserDTO)
async def get_user(user: UserDTO = Depends(provide_current_user)):
    return user
