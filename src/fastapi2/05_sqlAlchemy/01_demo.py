"""SQLAlchemy 2.x 异步 CRUD 示例。

默认连接本机 MySQL 的 ``customer_service_demo`` 数据库，运行时会自动创建
``sqlalchemy_crud_users`` 表，然后依次演示新增、查询、修改和删除。

PowerShell 运行示例：

    $env:MYSQL_PASSWORD = "你的密码"
    python src/fastapi2/05_sqlAlchemy/01_demo.py
"""

import asyncio
import os
from dataclasses import dataclass
from getpass import getpass

from sqlalchemy import URL, String, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    """数据库连接配置。"""

    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def server_url(self) -> URL:
        """生成不指定数据库的连接地址，用于首次建库。"""

        return URL.create(
            drivername="mysql+asyncmy",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            query={"charset": "utf8mb4"},
        )

    @property
    def database_url(self) -> URL:
        """生成业务数据库连接地址。"""

        return self.server_url.set(database=self.database)


def load_database_config() -> DatabaseConfig:
    """从环境变量读取配置；未提供密码时在终端安全输入。"""

    password = os.getenv("MYSQL_PASSWORD") or getpass("请输入 MySQL 密码: ")
    return DatabaseConfig(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "xiguapi"),
        password=password,
        database=os.getenv("MYSQL_DATABASE", "customer_service_demo"),
    )


class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""


class User(Base):
    """用于演示 CRUD 的用户表。"""

    __tablename__ = "sqlalchemy_crud_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"


async def create_database(config: DatabaseConfig) -> None:
    """数据库不存在时自动创建；账号需要具有 CREATE 权限。"""

    valid_name = config.database.replace("_", "")
    if not valid_name.isascii() or not valid_name.isalnum():
        raise ValueError("MYSQL_DATABASE 只能包含英文字母、数字和下划线")

    engine = create_async_engine(config.server_url, echo=False)
    try:
        async with engine.begin() as connection:
            database_exists = await connection.scalar(
                text("SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :database"),
                {"database": config.database},
            )
            if database_exists is None:
                await connection.execute(
                    text(f"CREATE DATABASE `{config.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                )
    finally:
        await engine.dispose()


async def create_user(session: AsyncSession, *, name: str, email: str) -> User:
    """新增一名用户。"""

    user = User(name=name, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    """按照主键查询用户。"""

    return await session.get(User, user_id)


async def list_users(session: AsyncSession) -> list[User]:
    """查询全部用户。"""

    result = await session.scalars(select(User).order_by(User.id))
    return list(result)


async def update_user(session: AsyncSession, user_id: int, *, name: str) -> User | None:
    """修改用户姓名。"""

    user = await session.get(User, user_id)
    if user is None:
        return None

    user.name = name
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    """删除指定用户。"""

    user = await session.get(User, user_id)
    if user is None:
        return False

    await session.delete(user)
    await session.commit()
    return True


async def main() -> None:
    """初始化数据表并按顺序执行 CRUD。"""

    config = load_database_config()
    await create_database(config)

    engine = create_async_engine(config.database_url, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        async with session_factory() as session:
            email = "sqlalchemy_demo@example.com"

            # 保证示例可以重复运行：先清理上次异常中断时可能留下的同名数据。
            old_user = await session.scalar(select(User).where(User.email == email))
            if old_user is not None:
                await session.delete(old_user)
                await session.commit()

            created = await create_user(session, name="张三", email=email)
            print("新增：", created)

            found = await get_user(session, created.id)
            print("查询单个：", found)
            print("查询全部：", await list_users(session))

            updated = await update_user(session, created.id, name="张三（已修改）")
            print("修改：", updated)

            deleted = await delete_user(session, created.id)
            print("删除：", deleted)
            print("删除后查询：", await get_user(session, created.id))
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
