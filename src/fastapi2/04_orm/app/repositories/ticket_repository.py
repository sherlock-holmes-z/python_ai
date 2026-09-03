"""工单 Repository：集中实现主表查询、分页和关联加载策略。"""

from collections.abc import Mapping
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.ticket import SupportTicket


class TicketRepository:
    """只处理持久化，不提交事务，也不决定 HTTP 状态码。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, ticket: SupportTicket) -> SupportTicket:
        self._session.add(ticket)
        await self._session.flush()
        await self._session.refresh(ticket)
        return ticket

    async def get_by_id(
        self,
        ticket_id: int,
        *,
        include_messages: bool = False,
        for_update: bool = False,
    ) -> SupportTicket | None:
        statement: Select[tuple[SupportTicket]] = select(SupportTicket).where(SupportTicket.id == ticket_id)
        if include_messages:
            statement = statement.options(selectinload(SupportTicket.messages))
        if for_update:
            statement = statement.with_for_update()
        ticket: SupportTicket | None = await self._session.scalar(statement)
        return ticket

    async def list_page(
        self,
        *,
        offset: int,
        limit: int,
        status: str | None,
        customer_email: str | None,
    ) -> tuple[list[SupportTicket], int]:
        filters = []
        if status is not None:
            filters.append(SupportTicket.status == status)
        if customer_email is not None:
            filters.append(SupportTicket.customer_email == customer_email)

        data_statement = (
            select(SupportTicket)
            .where(*filters)
            .order_by(SupportTicket.created_at.desc(), SupportTicket.id.desc())
            .offset(offset)
            .limit(limit)
        )
        count_statement = select(func.count(SupportTicket.id)).where(*filters)

        tickets = list((await self._session.scalars(data_statement)).all())
        total = int((await self._session.scalar(count_statement)) or 0)
        return tickets, total

    async def update(self, ticket: SupportTicket, changes: Mapping[str, Any]) -> SupportTicket:
        for field, value in changes.items():
            setattr(ticket, field, value)
        await self._session.flush()
        await self._session.refresh(ticket)
        return ticket

    async def delete(self, ticket: SupportTicket) -> None:
        await self._session.delete(ticket)
        await self._session.flush()
