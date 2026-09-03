"""消息 Repository：所有查询都带 ticket_id，防止跨工单误操作子资源。"""

from collections.abc import Mapping
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import TicketMessage


class MessageRepository:
    """封装消息子表的数据访问细节。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, message: TicketMessage) -> TicketMessage:
        self._session.add(message)
        await self._session.flush()
        await self._session.refresh(message)
        return message

    async def get_by_id(
        self,
        ticket_id: int,
        message_id: int,
        *,
        for_update: bool = False,
    ) -> TicketMessage | None:
        statement = select(TicketMessage).where(
            TicketMessage.id == message_id,
            TicketMessage.ticket_id == ticket_id,
        )
        if for_update:
            statement = statement.with_for_update()
        message: TicketMessage | None = await self._session.scalar(statement)
        return message

    async def list_page(
        self,
        *,
        ticket_id: int,
        offset: int,
        limit: int,
    ) -> tuple[list[TicketMessage], int]:
        data_statement = (
            select(TicketMessage)
            .where(TicketMessage.ticket_id == ticket_id)
            .order_by(TicketMessage.created_at.asc(), TicketMessage.id.asc())
            .offset(offset)
            .limit(limit)
        )
        count_statement = select(func.count(TicketMessage.id)).where(TicketMessage.ticket_id == ticket_id)

        messages = list((await self._session.scalars(data_statement)).all())
        total = int((await self._session.scalar(count_statement)) or 0)
        return messages, total

    async def update(self, message: TicketMessage, changes: Mapping[str, Any]) -> TicketMessage:
        for field, value in changes.items():
            setattr(message, field, value)
        await self._session.flush()
        await self._session.refresh(message)
        return message

    async def delete(self, message: TicketMessage) -> None:
        await self._session.delete(message)
        await self._session.flush()
