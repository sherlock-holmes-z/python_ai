"""基于环境变量的应用配置。

连接信息与代码分离便于跨电脑和多环境部署；使用结构化 URL 还能正确转义密码中的特殊字符。
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Settings loaded from ``04_orm/.env`` and environment variables."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "FastAPI ORM CRUD"
    app_env: str = "development"
    log_level: str = "INFO"
    cache_ttl_seconds: int = Field(default=300, ge=1)

    mysql_host: str = "192.168.100.102"
    mysql_port: int = Field(default=3306, ge=1, le=65535)
    mysql_user: str = "fastapi_app"
    mysql_password: SecretStr = SecretStr("CHANGE_ME_MYSQL_PASSWORD")
    mysql_database: str = "fastapi_orm"

    postgres_host: str = "192.168.100.102"
    postgres_port: int = Field(default=5432, ge=1, le=65535)
    postgres_user: str = "fastapi_app"
    postgres_password: SecretStr = SecretStr("CHANGE_ME_POSTGRES_PASSWORD")
    postgres_database: str = "fastapi_orm"

    redis_host: str = "192.168.100.102"
    redis_port: int = Field(default=6379, ge=1, le=65535)
    redis_password: SecretStr | None = None
    redis_db: int = Field(default=0, ge=0)

    @field_validator("redis_password", mode="before")
    @classmethod
    def normalize_empty_redis_password(cls, value: object) -> object:
        """Treat an empty ``REDIS_PASSWORD`` as no authentication."""

        return None if value == "" else value

    @property
    def mysql_url(self) -> URL:
        """Build an escaped async MySQL connection URL."""

        return URL.create(
            drivername="mysql+asyncmy",
            username=self.mysql_user,
            password=self.mysql_password.get_secret_value(),
            host=self.mysql_host,
            port=self.mysql_port,
            database=self.mysql_database,
            query={"charset": "utf8mb4"},
        )

    @property
    def postgres_url(self) -> URL:
        """Build an escaped async PostgreSQL connection URL."""

        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_database,
        )

    @property
    def redis_password_value(self) -> str | None:
        """Return the Redis password without exposing it in repr output."""

        if self.redis_password is None:
            return None
        return self.redis_password.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    """Return one immutable-by-convention settings instance per process."""

    return Settings()
