"""SQLAlchemy ORM 模型导出入口。

显式导出模型可提供统一导入路径，也便于迁移工具一次加载完整的元数据。
"""

from app.models.mysql import Product
from app.models.postgresql import ProductAuditLog

__all__ = ["Product", "ProductAuditLog"]
