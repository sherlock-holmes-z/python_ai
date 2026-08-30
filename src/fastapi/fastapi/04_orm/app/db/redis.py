"""应用级异步 Redis 客户端。

客户端在应用生命周期内复用底层连接池，避免每次请求重复建立 TCP 连接造成额外开销。
"""

from collections.abc import AsyncIterator

from redis.asyncio import Redis

from app.core.config import get_settings

settings = get_settings()

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password_value,
    db=settings.redis_db,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
    health_check_interval=30,
)


async def get_redis_client() -> AsyncIterator[Redis]:
    """Inject the shared Redis connection pool backed client."""

    yield redis_client


async def close_redis_client() -> None:
    """Close the Redis client during application shutdown."""

    await redis_client.aclose()
