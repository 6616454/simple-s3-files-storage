from src.api.handlers.responses.user import BaseUser


class CreateUser(BaseUser):
    password: str
    password_correct: str
