from pydantic import BaseSettings


class Settings(BaseSettings):
    black_list: list[str] = []

    database_url: str
    echo_mode: bool = False

    redis_host: str
    redis_port: int = 6379
    redis_db: int = 1

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600  # Жизнь токена - часv

    class Config:
        env_file = '.env'


def get_settings() -> Settings:
    return Settings()
