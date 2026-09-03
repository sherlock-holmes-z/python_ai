"""FastAPI 应用入口：注册路由、统一异常处理，并在停机时释放连接池。"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import system, tickets
from app.core.config import settings
from app.core.exceptions import ApplicationError
from app.db.session import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """应用退出时关闭池中连接，开发环境热重载也不会遗留连接。"""

    logger.info("customer_service_api_started")
    yield
    await engine.dispose()
    logger.info("customer_service_api_stopped")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="基于 FastAPI、SQLAlchemy 2.x AsyncSession 和 MySQL 的客服工单教学项目。",
    lifespan=lifespan,
)


@app.exception_handler(ApplicationError)
async def handle_application_error(_request: Request, exc: ApplicationError) -> JSONResponse:
    """把可预期业务异常转换成统一响应，未知异常仍交给框架记录和处理。"""

    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(_request: Request, _exc: RequestValidationError) -> JSONResponse:
    """统一参数错误格式，使 OpenAPI 声明与客户端实际收到的 422 响应一致。"""

    return JSONResponse(
        status_code=422,
        content={"code": "REQUEST_VALIDATION_ERROR", "message": "请求参数校验失败"},
    )


app.include_router(system.router)
app.include_router(tickets.router, prefix=settings.api_v1_prefix)
