"""客服工单应用服务：组织业务规则、事务边界以及主子表协作。"""

from math import ceil
from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidOperationError, ResourceConflictError, ResourceNotFoundError
from app.models.message import TicketMessage
from app.models.ticket import SupportTicket
from app.repositories.message_repository import MessageRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.common import PageResponse
from app.schemas.message import MessageCreate, MessageResponse, MessageUpdate
from app.schemas.ticket import TicketCreate, TicketDetailResponse, TicketResponse, TicketUpdate


class TicketService:
    """以一次用例为一个事务，Repository 不会自行提交造成半完成状态。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._tickets = TicketRepository(session)
        self._messages = MessageRepository(session)

    async def create_ticket(self, payload: TicketCreate) -> TicketResponse:
        ticket = SupportTicket(
            ticket_no=f"CS-{uuid4().hex[:12].upper()}",
            **payload.model_dump(mode="json"),
        )
        try:
            async with self._session.begin():
                await self._tickets.create(ticket)
        except IntegrityError as exc:
            raise ResourceConflictError("工单编号冲突，请重试") from exc
        return TicketResponse.model_validate(ticket)

    async def get_ticket(self, ticket_id: int) -> TicketDetailResponse:
        ticket = await self._tickets.get_by_id(ticket_id, include_messages=True)
        if ticket is None:
            raise ResourceNotFoundError("工单不存在")
        return TicketDetailResponse.model_validate(ticket)

    async def list_tickets(
        self,
        *,
        page: int,
        page_size: int,
        status: str | None,
        customer_email: str | None,
    ) -> PageResponse[TicketResponse]:
        tickets, total = await self._tickets.list_page(
            offset=(page - 1) * page_size,
            limit=page_size,
            status=status,
            customer_email=customer_email,
        )
        return PageResponse[TicketResponse](
            items=[TicketResponse.model_validate(ticket) for ticket in tickets],
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if total else 0,
        )

    async def update_ticket(self, ticket_id: int, payload: TicketUpdate) -> TicketResponse:
        changes = payload.model_dump(exclude_unset=True, mode="json")
        if not changes:
            raise InvalidOperationError("至少提供一个需要修改的工单字段")

        async with self._session.begin():
            ticket = await self._tickets.get_by_id(ticket_id, for_update=True)
            if ticket is None:
                raise ResourceNotFoundError("工单不存在")
            await self._tickets.update(ticket, changes)
        return TicketResponse.model_validate(ticket)

    async def delete_ticket(self, ticket_id: int) -> None:
        async with self._session.begin():
            ticket = await self._tickets.get_by_id(ticket_id, for_update=True)
            if ticket is None:
                raise ResourceNotFoundError("工单不存在")
            await self._tickets.delete(ticket)

    async def create_message(self, ticket_id: int, payload: MessageCreate) -> MessageResponse:
        async with self._session.begin():
            ticket = await self._tickets.get_by_id(ticket_id, for_update=True)
            if ticket is None:
                raise ResourceNotFoundError("工单不存在，不能新增消息")
            message = TicketMessage(ticket_id=ticket_id, **payload.model_dump(mode="json"))
            await self._messages.create(message)
        return MessageResponse.model_validate(message)

    async def get_message(self, ticket_id: int, message_id: int) -> MessageResponse:
        message = await self._messages.get_by_id(ticket_id, message_id)
        if message is None:
            raise ResourceNotFoundError("工单消息不存在")
        return MessageResponse.model_validate(message)

    async def list_messages(
        self,
        *,
        ticket_id: int,
        page: int,
        page_size: int,
    ) -> PageResponse[MessageResponse]:
        if await self._tickets.get_by_id(ticket_id) is None:
            raise ResourceNotFoundError("工单不存在")
        messages, total = await self._messages.list_page(
            ticket_id=ticket_id,
            offset=(page - 1) * page_size,
            limit=page_size,
        )
        return PageResponse[MessageResponse](
            items=[MessageResponse.model_validate(message) for message in messages],
            total=total,
            page=page,
            page_size=page_size,
            pages=ceil(total / page_size) if total else 0,
        )

    async def update_message(
        self,
        ticket_id: int,
        message_id: int,
        payload: MessageUpdate,
    ) -> MessageResponse:
        changes = payload.model_dump(exclude_unset=True)
        if not changes:
            raise InvalidOperationError("至少提供一个需要修改的消息字段")

        async with self._session.begin():
            message = await self._messages.get_by_id(ticket_id, message_id, for_update=True)
            if message is None:
                raise ResourceNotFoundError("工单消息不存在")
            await self._messages.update(message, changes)
        return MessageResponse.model_validate(message)

    async def delete_message(self, ticket_id: int, message_id: int) -> None:
        async with self._session.begin():
            message = await self._messages.get_by_id(ticket_id, message_id, for_update=True)
            if message is None:
                raise ResourceNotFoundError("工单消息不存在")
            await self._messages.delete(message)
