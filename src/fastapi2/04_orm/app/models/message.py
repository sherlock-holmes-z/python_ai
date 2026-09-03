"""客服沟通消息子表模型；每条消息必须归属于一张有效工单。"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.ticket import SupportTicket


class TicketMessage(Base):
    """工单中的一次客户、客服或系统留言。"""

    __tablename__ = "ticket_messages"
    __table_args__ = (
        CheckConstraint(
            "sender_type IN ('customer', 'agent', 'system')",
            name="sender_type_values",
        ),
        Index("ix_ticket_messages_ticket_id_created_at", "ticket_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ticket_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("support_tickets.id", ondelete="CASCADE"),
        nullable=False,
    )
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)
    sender_name: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    ticket: Mapped["SupportTicket"] = relationship(back_populates="messages")
