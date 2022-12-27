from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class CreateUser(BaseUser):
    password: str
    password_correct: str


class UserSchema(BaseUser):
    id: int
    user_path: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
