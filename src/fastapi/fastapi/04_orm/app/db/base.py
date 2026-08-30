"""两个数据库各自独立的 SQLAlchemy 元数据注册表。

MySQL 与 PostgreSQL 分开建模，可防止迁移或建表工具把某个数据库的表误建到另一个数据库。
"""

from sqlalchemy.orm import DeclarativeBase


class MySQLBase(DeclarativeBase):
    """Base class for tables stored in MySQL."""


class PostgreSQLBase(DeclarativeBase):
    """Base class for tables stored in PostgreSQL."""
