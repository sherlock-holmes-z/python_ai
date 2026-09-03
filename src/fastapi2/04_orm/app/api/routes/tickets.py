"""客服工单 HTTP 接口：包含主子表 CRUD、数据库分页和关联详情查询。"""

from typing import Annotated, Any

from fastapi import APIRouter, Path, Query, Response, status

from app.api.dependencies import TicketServiceDep
from app.models.enums import TicketStatus
from app.schemas.common import ErrorResponse, PageResponse
from app.schemas.message import MessageCreate, MessageResponse, MessageUpdate
from app.schemas.ticket import TicketCreate, TicketDetailResponse, TicketResponse, TicketUpdate

router = APIRouter(prefix="/tickets", tags=["客服工单"])

TicketId = Annotated[int, Path(ge=1, description="工单主键")]
MessageId = Annotated[int, Path(ge=1, description="消息主键")]
PageNumber = Annotated[int, Query(ge=1, description="页码，从 1 开始")]
PageSize = Annotated[int, Query(ge=1, le=100, description="每页条数，最大 100")]

ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    404: {"model": ErrorResponse, "description": "资源不存在"},
    409: {"model": ErrorResponse, "description": "资源冲突"},
    422: {"model": ErrorResponse, "description": "参数或业务校验失败"},
}


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
)
async def create_ticket(payload: TicketCreate, service: TicketServiceDep) -> TicketResponse:
    """创建工单，工单编号由服务端生成。"""

    return await service.create_ticket(payload)


@router.get("", response_model=PageResponse[TicketResponse])
async def list_tickets(
    service: TicketServiceDep,
    page: PageNumber = 1,
    page_size: PageSize = 20,
    ticket_status: Annotated[TicketStatus | None, Query(alias="status")] = None,
    customer_email: Annotated[str | None, Query(min_length=3, max_length=254)] = None,
) -> PageResponse[TicketResponse]:
    """分页查询工单，可按状态和客户邮箱过滤。"""

    return await service.list_tickets(
        page=page,
        page_size=page_size,
        status=ticket_status.value if ticket_status else None,
        customer_email=customer_email,
    )


@router.get("/{ticket_id}", response_model=TicketDetailResponse, responses=ERROR_RESPONSES)
async def get_ticket(ticket_id: TicketId, service: TicketServiceDep) -> TicketDetailResponse:
    """关联查询一张工单及其全部消息，避免 ORM 懒加载引发异步错误。"""

    return await service.get_ticket(ticket_id)


@router.patch("/{ticket_id}", response_model=TicketResponse, responses=ERROR_RESPONSES)
async def update_ticket(
    ticket_id: TicketId,
    payload: TicketUpdate,
    service: TicketServiceDep,
) -> TicketResponse:
    """局部更新工单，只覆盖请求中明确提供的字段。"""

    return await service.update_ticket(ticket_id, payload)


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=ERROR_RESPONSES,
)
async def delete_ticket(ticket_id: TicketId, service: TicketServiceDep) -> Response:
    """删除工单；数据库外键 ON DELETE CASCADE 会同时删除所属消息。"""

    await service.delete_ticket(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{ticket_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
)
async def create_message(
    ticket_id: TicketId,
    payload: MessageCreate,
    service: TicketServiceDep,
) -> MessageResponse:
    """在指定工单下新增一条沟通消息。"""

    return await service.create_message(ticket_id, payload)


@router.get(
    "/{ticket_id}/messages",
    response_model=PageResponse[MessageResponse],
    responses=ERROR_RESPONSES,
)
async def list_messages(
    ticket_id: TicketId,
    service: TicketServiceDep,
    page: PageNumber = 1,
    page_size: PageSize = 20,
) -> PageResponse[MessageResponse]:
    """分页查询一张工单的消息。"""

    return await service.list_messages(ticket_id=ticket_id, page=page, page_size=page_size)


@router.get(
    "/{ticket_id}/messages/{message_id}",
    response_model=MessageResponse,
    responses=ERROR_RESPONSES,
)
async def get_message(
    ticket_id: TicketId,
    message_id: MessageId,
    service: TicketServiceDep,
) -> MessageResponse:
    """查询一条属于指定工单的消息。"""

    return await service.get_message(ticket_id, message_id)


@router.patch(
    "/{ticket_id}/messages/{message_id}",
    response_model=MessageResponse,
    responses=ERROR_RESPONSES,
)
async def update_message(
    ticket_id: TicketId,
    message_id: MessageId,
    payload: MessageUpdate,
    service: TicketServiceDep,
) -> MessageResponse:
    """修正指定工单下的消息内容。"""

    return await service.update_message(ticket_id, message_id, payload)


@router.delete(
    "/{ticket_id}/messages/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=ERROR_RESPONSES,
)
async def delete_message(
    ticket_id: TicketId,
    message_id: MessageId,
    service: TicketServiceDep,
) -> Response:
    """删除一条属于指定工单的消息。"""

    await service.delete_message(ticket_id, message_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
