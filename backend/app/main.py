import logging

from fastapi import FastAPI

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.users import router as users_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.cors import configure_cors

configure_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
    )

    configure_cors(app)
    register_exception_handlers(app)

    app.include_router(health_router)
    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(users_router, prefix=settings.API_V1_PREFIX)

    @app.get("/", tags=["Root"])
    async def root() -> dict:
        return {
            "message": settings.PROJECT_NAME,
            "version": settings.VERSION,
        }

    @app.on_event("startup")
    async def on_startup() -> None:
        logger.info(
            "Starting %s v%s in %s mode",
            settings.PROJECT_NAME,
            settings.VERSION,
            settings.ENVIRONMENT,
        )

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        logger.info("Shutting down %s", settings.PROJECT_NAME)

    return app


app = create_app()
