"""FastAPI 应用入口。

这里只负责组装路由、异常处理器和生命周期资源，使业务逻辑不依赖应用启动方式。
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse

from app.api.routes.health import router as health_router
from app.api.routes.products import router as products_router
from app.core.config import get_settings
from app.core.exceptions import DuplicateSkuError, ProductNotFoundError
from app.db.mysql import mysql_engine
from app.db.postgresql import postgresql_engine
from app.db.redis import close_redis_client
from fastapi import FastAPI, Request, status

settings = get_settings()

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Release application-scoped connection pools on shutdown."""

    yield
    await close_redis_client()
    await mysql_engine.dispose()
    await postgresql_engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(
    _request: Request,
    exc: ProductNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(DuplicateSkuError)
async def duplicate_sku_handler(
    _request: Request,
    exc: DuplicateSkuError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


app.include_router(health_router)
app.include_router(products_router, prefix="/api/v1")
