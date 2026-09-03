"""集中读取环境配置，避免把账号、密码和连接参数硬编码进业务代码。"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

PROJECT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """应用配置；环境变量优先级高于项目目录中的 .env。"""

    model_config = SettingsConfigDict(
        env_file=PROJECT_DIR / ".env",
        env_file_encoding="utf-8",
        env_prefix="CUSTOMER_SERVICE_",
        extra="ignore",
    )

    app_name: str = "客服工单 API"
    api_v1_prefix: str = "/api/v1"
    db_host: str = "127.0.0.1"
    db_port: int = Field(default=3306, ge=1, le=65535)
    db_user: str = "xiguapi"
    db_password: str
    db_name: str = "customer_service_demo"
    db_pool_size: int = Field(default=10, ge=1)
    db_max_overflow: int = Field(default=20, ge=0)
    db_pool_recycle_seconds: int = Field(default=1800, ge=60)
    sql_echo: bool = False

    @property
    def sqlalchemy_database_uri(self) -> URL:
        """用 URL.create 组装地址，密码含特殊字符时也能正确转义。"""

        return URL.create(
            drivername="mysql+asyncmy",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={"charset": "utf8mb4"},
        )


@lru_cache
def get_settings() -> Settings:
    """配置只解析一次，保证整个进程使用一致的连接参数。"""

    return Settings()  # type: ignore[call-arg]


settings = get_settings()
