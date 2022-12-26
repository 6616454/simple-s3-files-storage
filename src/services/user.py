import datetime
import logging
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from passlib.handlers.bcrypt import bcrypt

from sqlalchemy.exc import IntegrityError
from starlette import status

from src.core.config import Settings
from src.db.repositories.holder import HolderRepository
from src.dto.user import UserDTO, Token, CreateUser

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')

logger = logging.getLogger('main_logger')


class UserService:

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @staticmethod
    async def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    def __init__(
            self,
            settings: Optional[Settings] = None
    ):
        self.settings: Settings = settings

    async def create_token(self, user: UserDTO) -> Token:

        now = datetime.datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + datetime.timedelta(seconds=self.settings.jwt_expiration),
            'sub': str(user.id),
            'user': user.dict(),
        }
        token = jwt.encode(
            payload,
            self.settings.jwt_secret,
            algorithm=self.settings.jwt_algorithm
        )

        return Token(access_token=token)

    async def validate_token(self, token: str) -> UserDTO:
        try:
            payload = jwt.decode(
                token,
                self.settings.jwt_secret,
                algorithms=[self.settings.jwt_algorithm]
            )
        except JWTError:
            logger.warning('User use invalid token %s', token)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access Token was expired')

        user_data = payload.get('user')

        user = UserDTO.parse_obj(user_data)

        return user

    async def register_new_user(self, user_data: CreateUser, uow: HolderRepository) -> Token:

        if user_data.password == user_data.password_correct:

            try:
                user = await uow.user_repo.create_user(
                    username=user_data.username,
                    password_hash=await self.hash_password(user_data.password)
                )

                logger.info('Create new User %s', user_data.username)

                return await self.create_token(user.to_user_schema())
            except IntegrityError:
                logger.warning('Invalid registration')
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Username is already in use')

        logger.warning('Invalid registration')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credentials not valid')

    async def authenticate_user(self, username: str, password: str, uow: HolderRepository) -> Token:

        user = await uow.user_repo.get_user_by_name(username=username)

        if not user:
            logger.warning('Invalid authentication for username %s', username)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Username or password not valid')

        if not await self.verify_password(password, user.password_hash):
            logger.warning('Invalid authentication for user %s', username)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Username or password not valid')

        logger.info('Valid authentication user - %s', username)
        return await self.create_token(user.to_user_schema())

    async def get_current_user(self, token: str = Depends(oauth_scheme)) -> UserDTO:
        return await self.validate_token(token)
