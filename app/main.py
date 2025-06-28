"""Main FastAPI application entrypoint.

Provides a minimal health endpoint and registers versioned API routers.
Lifespan handler prepares global resources (e.g. OpenAI client) in future.
"""

from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys

from fastapi import APIRouter, FastAPI
from loguru import logger

from app.core.settings import settings

# ---------------------------------------------------------------------------
# API Routers
# ---------------------------------------------------------------------------

api_router = APIRouter(prefix="/api")


# ---------------------------------------------------------------------------
# FastAPI application factory
# ---------------------------------------------------------------------------


def create_app() -> FastAPI:
    """Instantiate FastAPI app and include routers."""

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        logger.info("Backend started and ready to accept requests")
        yield
        logger.info("Shutting down backend")

    # --- LOGGING CONFIG ---
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"backend_api_{current_date}.log")
    logger.remove()
    log_level = "DEBUG"
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    logger.add(
        log_file,
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    logger.info(f"Backend logging configured: {log_file} (level={log_level})")

    app = FastAPI(
        title="Entity Extraction & Knowledge API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Mount v1 routers
    from app.api.v1 import compendium as compendium_v1
    from app.api.v1 import linker as linker_v1
    from app.api.v1 import pipeline as pipeline_v1
    from app.api.v1 import qa as qa_v1
    from app.api.v1 import utils as utils_v1

    api_router.include_router(linker_v1.router)
    api_router.include_router(compendium_v1.router)
    api_router.include_router(qa_v1.router)
    api_router.include_router(utils_v1.router)
    api_router.include_router(pipeline_v1.router)

    # Add rate limiter middleware
    from app.middleware.ratelimiter import RateLimitMiddleware

    app.add_middleware(
        RateLimitMiddleware,
        limit=settings.RATE_LIMIT,
        window=settings.RATE_WINDOW,
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint for monitoring and Docker health checks."""
        return {
            "status": "healthy",
            "service": "entityextractorbatch",
            "version": "0.1.0",
            "timestamp": "2025-06-23T10:30:00Z"
        }

    # Register top-level api router
    app.include_router(api_router)

    return app


app = create_app()

# For `uvicorn backend.app.main:app --reload`
__all__ = ["app"]
