from pydantic import BaseSettings


class Settings(BaseSettings):
    black_list: list[str] = []

    database_url: str
    echo_mode: bool = False

    redis_host: str
    redis_port: int = 6379
    redis_db: int = 1

    s3_host: str
    minio_root_user: str
    minio_root_password: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 60 * 60

    class Config:
        env_file = '.env'


def get_settings() -> Settings:
    return Settings()
