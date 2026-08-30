"""运行时依赖健康检查。

主动探测三个外部服务，便于部署平台判断实例是否可用，同时不向客户端泄露连接凭据和底层异常。
"""

from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import MySQLSessionDep, PostgreSQLSessionDep, RedisDep
from app.schemas.health import HealthResponse
from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check(
    response: Response,
    mysql_session: MySQLSessionDep,
    postgresql_session: PostgreSQLSessionDep,
    redis: RedisDep,
) -> HealthResponse:
    dependency_status: dict[str, str] = {
        "mysql": "down",
        "postgresql": "down",
        "redis": "down",
    }

    try:
        await mysql_session.execute(text("SELECT 1"))
        dependency_status["mysql"] = "up"
    except SQLAlchemyError:
        pass

    try:
        await postgresql_session.execute(text("SELECT 1"))
        dependency_status["postgresql"] = "up"
    except SQLAlchemyError:
        pass

    try:
        await redis.ping()
        dependency_status["redis"] = "up"
    except RedisError:
        pass

    all_healthy = all(value == "up" for value in dependency_status.values())
    if not all_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthResponse(
        status="ok" if all_healthy else "degraded",
        dependencies=dependency_status,  # type: ignore[arg-type]
    )
