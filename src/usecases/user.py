import datetime
import logging
import uuid

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from passlib.handlers.bcrypt import bcrypt

from sqlalchemy.exc import IntegrityError
from starlette import status

from src.api.handlers.requests.user import CreateUser
from src.api.handlers.responses.user import UserSchema, Token
from src.infrastructure.db.repositories.s3 import S3Repository
from src.infrastructure.db.repositories.user import UserRepository

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
        jwt_expiration,
        jwt_secret: str,
        jwt_algorithm: str
    ):
        self.jwt_expiration = jwt_expiration
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm

    async def create_token(self, user: UserSchema) -> Token:

        now = datetime.datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + datetime.timedelta(seconds=self.jwt_expiration),
            'sub': str(user.id),
            'user': user.dict(),
        }
        token = jwt.encode(
            payload,
            self.jwt_secret,
            algorithm=self.jwt_algorithm
        )

        return Token(access_token=token)

    async def validate_token(self, token: str) -> UserSchema:
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )
        except JWTError:
            logger.warning('User use invalid token %s', token)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Access Token was expired')

        user_data = payload.get('user')

        user = UserSchema.parse_obj(user_data)

        return user

    async def register_new_user(
        self,
        user_data: CreateUser,
        user_repo: UserRepository,
        s3_repo: S3Repository,
    ) -> Token:

        if user_data.password == user_data.password_correct:

            _uuid = str(uuid.uuid4())

            try:
                user = await user_repo.create_user(
                    username=user_data.username,
                    password_hash=await self.hash_password(user_data.password),
                    user_path=_uuid

                )

                await user_repo.commit()

                logger.info('Create new User %s', user_data.username)

                await s3_repo.create_bucket(_uuid)

                return await self.create_token(user.to_user_schema())
            except IntegrityError:
                logger.warning('Invalid registration')
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Username is already in use')

        logger.warning('Invalid registration')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credentials not valid')

    async def authenticate_user(self, username: str, password: str,
                                user_repo: UserRepository) -> Token:

        user = await user_repo.get_user_by_name(username=username)

        if not user:
            logger.warning('Invalid authentication for username %s', username)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Username or password not valid')

        if not await self.verify_password(password, user.password_hash):
            logger.warning('Invalid authentication for user %s', username)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Username or password not valid')

        logger.info('Valid authentication user - %s', username)
        return await self.create_token(user.to_user_schema())

    async def get_current_user(self, token: str = Depends(oauth_scheme)) -> UserSchema:
        return await self.validate_token(token)
