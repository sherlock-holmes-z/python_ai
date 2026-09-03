"""领域枚举统一定义在一处，接口校验与数据库模型共享同一组合法值。"""

from enum import StrEnum


class TicketStatus(StrEnum):
    """工单生命周期状态。"""

    OPEN = "open"
    PROCESSING = "processing"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(StrEnum):
    """工单优先级。"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class MessageSenderType(StrEnum):
    """消息发送方类型。"""

    CUSTOMER = "customer"
    AGENT = "agent"
    SYSTEM = "system"
