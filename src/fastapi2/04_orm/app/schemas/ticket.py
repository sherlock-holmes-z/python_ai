"""工单接口 DTO，区分创建、局部更新、列表摘要和关联详情。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TicketPriority, TicketStatus
from app.schemas.message import MessageResponse


class TicketCreate(BaseModel):
    """新建工单时由服务端生成工单编号和初始状态。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    customer_name: str = Field(min_length=1, max_length=100)
    customer_email: str = Field(min_length=3, max_length=254)
    subject: str = Field(min_length=1, max_length=200)
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketUpdate(BaseModel):
    """PATCH 请求模型；未提供的字段不会覆盖数据库现值。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    customer_name: str | None = Field(default=None, min_length=1, max_length=100)
    customer_email: str | None = Field(default=None, min_length=3, max_length=254)
    subject: str | None = Field(default=None, min_length=1, max_length=200)
    status: TicketStatus | None = None
    priority: TicketPriority | None = None


class TicketResponse(BaseModel):
    """工单列表和普通 CRUD 使用的轻量响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_no: str
    customer_name: str
    customer_email: str
    subject: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime


class TicketDetailResponse(TicketResponse):
    """关联查询响应，在工单字段之外一次性返回有序消息列表。"""

    messages: list[MessageResponse]
