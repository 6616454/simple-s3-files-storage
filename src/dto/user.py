from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class CreateUser(BaseUser):
    password: str
    password_correct: str


class UserDTO(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
