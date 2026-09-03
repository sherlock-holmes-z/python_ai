"""消息接口 DTO，只暴露业务需要的字段，避免直接接收 ORM 对象。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import MessageSenderType


class MessageCreate(BaseModel):
    """创建一条工单消息。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    sender_type: MessageSenderType
    sender_name: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=10_000)


class MessageUpdate(BaseModel):
    """示例允许修正发送人名称和消息正文，不允许更改所属工单。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    sender_name: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1, max_length=10_000)


class MessageResponse(BaseModel):
    """消息输出模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int
    sender_type: MessageSenderType
    sender_name: str
    content: str
    created_at: datetime
    updated_at: datetime
