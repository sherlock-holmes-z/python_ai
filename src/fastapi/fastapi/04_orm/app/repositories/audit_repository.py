"""PostgreSQL 审计仓储。

把审计日志写入细节隔离在独立仓储中，业务服务只需表达何时记录以及记录什么。
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.postgresql import ProductAuditLog


class ProductAuditRepository:
    """Persist product mutation audit events in PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        product_id: int,
        action: str,
        payload: dict[str, Any],
    ) -> ProductAuditLog:
        event = ProductAuditLog(
            product_id=product_id,
            action=action,
            payload=payload,
        )
        self.session.add(event)
        await self.session.flush()
        return event
