import logging

from fastapi import APIRouter, status
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine
from app.schemas.response import success_response

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict:
    return success_response(
        data={
            "status": "ok",
            "environment": settings.ENVIRONMENT,
            "version": settings.VERSION,
        },
        message="Service is running.",
    )


@router.get("/health/db", status_code=status.HTTP_200_OK)
async def health_check_db() -> dict:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return success_response(
            data={"status": "ok", "database": "reachable"},
            message="Database connection successful.",
        )
    except Exception as exc:  # noqa: BLE001 - deliberately broad for a health check
        logger.error("Database health check failed: %s", exc)
        return success_response(
            data={"status": "error", "database": "unreachable"},
            message="Database connection failed.",
        )
