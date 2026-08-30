"""可复用的 FastAPI 依赖声明。

集中组装数据库会话、Redis 客户端和业务服务，避免每个路由重复创建基础设施对象。
"""

from typing import Annotated

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_mysql_session
from app.db.postgresql import get_postgresql_session
from app.db.redis import get_redis_client
from app.services.product_service import ProductService
from fastapi import Depends

MySQLSessionDep = Annotated[AsyncSession, Depends(get_mysql_session)]
PostgreSQLSessionDep = Annotated[AsyncSession, Depends(get_postgresql_session)]
RedisDep = Annotated[Redis, Depends(get_redis_client)]


def get_product_service(
    mysql_session: MySQLSessionDep,
    postgresql_session: PostgreSQLSessionDep,
    redis: RedisDep,
) -> ProductService:
    return ProductService(
        mysql_session=mysql_session,
        postgresql_session=postgresql_session,
        redis=redis,
    )


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
