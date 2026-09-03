"""SQLAlchemy 模型统一出口，确保元数据收集到全部数据表。"""

from app.models.message import TicketMessage
from app.models.ticket import SupportTicket

__all__ = ["SupportTicket", "TicketMessage"]
