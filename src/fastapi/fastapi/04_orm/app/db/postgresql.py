"""PostgreSQL 异步引擎和请求级会话依赖。

审计库使用独立连接池与会话，避免和 MySQL 主数据事务混用，从结构上明确数据源边界。
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

postgresql_engine = create_async_engine(
    settings.postgres_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={"timeout": 3},
)

PostgreSQLSessionFactory = async_sessionmaker(
    bind=postgresql_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_postgresql_session() -> AsyncIterator[AsyncSession]:
    """Yield one PostgreSQL session for one request/dependency execution."""

    async with PostgreSQLSessionFactory() as session:
        yield session
