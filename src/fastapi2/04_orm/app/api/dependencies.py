"""依赖注入组装点，把请求级数据库会话注入应用服务。"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.services.ticket_service import TicketService

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_ticket_service(session: SessionDep) -> TicketService:
    """每个请求创建轻量 Service，内部共享同一个请求级会话。"""

    return TicketService(session)


TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]
