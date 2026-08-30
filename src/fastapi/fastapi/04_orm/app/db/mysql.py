"""MySQL 异步引擎和请求级会话依赖。

进程内复用连接池以降低建连成本，每个请求使用独立会话以隔离事务和异常状态。
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

mysql_engine = create_async_engine(
    settings.mysql_url,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=10,
    max_overflow=20,
    connect_args={"connect_timeout": 3},
)

MySQLSessionFactory = async_sessionmaker(
    bind=mysql_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_mysql_session() -> AsyncIterator[AsyncSession]:
    """Yield one MySQL session for one request/dependency execution."""

    async with MySQLSessionFactory() as session:
        yield session
