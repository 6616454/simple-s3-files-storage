import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import setup_routes
from src.core.config import get_settings
from src.core.logging import setup_logging
from src.infrastructure.db.base import create_pool, create_redis, create_s3
from src.api.di import setup_dependency_injection
from src.api.middlewares import setup_middlewares


def build_app() -> FastAPI:
    settings = get_settings()

    pool = create_pool(settings.database_url, settings.echo_mode)

    app = FastAPI(
        default_response_class=ORJSONResponse
    )

    setup_middlewares(app, settings)
    setup_dependency_injection(
        app=app,
        pool=pool,
        redis=create_redis(settings.redis_host, settings.redis_port, settings.redis_db),
        s3_session=create_s3(),
        settings=settings
    )
    setup_routes(app.router)
    setup_logging()

    return app


if __name__ == '__main__':
    uvicorn.run(
        'src.main:build_app',
        factory=True,
        reload=True,
        host='0.0.0.0'
    )
