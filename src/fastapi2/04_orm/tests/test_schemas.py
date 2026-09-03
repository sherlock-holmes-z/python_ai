"""验证 DTO 的禁止额外字段和局部更新语义，防止接口静默接收拼错的字段。"""

import pytest
from pydantic import ValidationError

from app.models.enums import TicketPriority
from app.schemas.ticket import TicketCreate, TicketUpdate


def test_ticket_create_uses_default_priority_and_strips_whitespace() -> None:
    payload = TicketCreate(
        customer_name="  张三  ",
        customer_email="zhangsan@example.com",
        subject="  无法登录  ",
    )

    assert payload.customer_name == "张三"
    assert payload.subject == "无法登录"
    assert payload.priority is TicketPriority.MEDIUM


def test_ticket_create_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        TicketCreate(
            customer_name="张三",
            customer_email="zhangsan@example.com",
            subject="无法登录",
            unknown_field="should-fail",  # type: ignore[call-arg]
        )


def test_patch_only_exports_explicit_fields() -> None:
    payload = TicketUpdate(status="resolved")

    assert payload.model_dump(exclude_unset=True, mode="json") == {"status": "resolved"}
