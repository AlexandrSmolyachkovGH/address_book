from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import (
    FastAPI,
    status,
)
from redis.asyncio import (
    ConnectionPool,
    Redis,
)

from app.book.routers import book_router
from app.custom_exceptions.custom_exceptions import (
    ServiceError,
)
from app.custom_exceptions.exception_handlers import (
    service_error_handler,
)
from app.settings.redis_settings import redis_settings
from app.text_samples.root import RootPageTexts


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator:
    pool = ConnectionPool.from_url(
        redis_settings.redis_dsn,
        max_connections=50,
        decode_responses=True,
    )
    application.state.redis = Redis.from_pool(pool)
    try:
        yield
    finally:
        await application.state.redis.aclose()


app = FastAPI(lifespan=lifespan)

# Routers
app.include_router(router=book_router)

# Exception handlers
app.add_exception_handler(ServiceError, service_error_handler)


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    description="API representation and common links",
)
async def get_root() -> dict:
    return {
        "title": RootPageTexts.get_root_title(),
        "description": RootPageTexts.get_root_description(),
        "paths": {
            "swagger": "/docs",
            "redoc": "/redoc",
        },
    }
