import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import setup_routes
from src.core.config import get_settings
from src.core.logging import setup_logging
from src.db.models.base import create_pool
from src.di import setup_dependency_injection
from src.middlewares import setup_middlewares


def build_app() -> FastAPI:
    settings = get_settings()

    pool = create_pool(settings.database_url, settings.echo_mode)

    app = FastAPI(
        default_response_class=ORJSONResponse
    )

    setup_middlewares(app, settings)
    setup_dependency_injection(app, pool, settings)
    setup_routes(app.router)
    setup_logging()

    return app


if __name__ == '__main__':
    uvicorn.run(
        'src.main:build_app',
        factory=True,
        reload=True,
    )
