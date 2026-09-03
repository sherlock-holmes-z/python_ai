"""验证路由能成功生成 OpenAPI，并覆盖主子资源的关键操作。"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


def test_openapi_contains_ticket_crud_and_relation_query() -> None:
    schema = app.openapi()
    paths = schema["paths"]

    assert {"get", "post"} <= paths["/api/v1/tickets"].keys()
    assert {"get", "patch", "delete"} <= paths["/api/v1/tickets/{ticket_id}"].keys()
    assert {"get", "post"} <= paths["/api/v1/tickets/{ticket_id}/messages"].keys()
    assert {"get", "patch", "delete"} <= paths["/api/v1/tickets/{ticket_id}/messages/{message_id}"].keys()


def test_pagination_constraints_are_published() -> None:
    operation = app.openapi()["paths"]["/api/v1/tickets"]["get"]
    parameters = {parameter["name"]: parameter for parameter in operation["parameters"]}

    assert parameters["page"]["schema"]["minimum"] == 1
    assert parameters["page_size"]["schema"]["maximum"] == 100


@pytest.mark.asyncio
async def test_validation_error_uses_unified_error_shape() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/tickets", json={"customer_name": "张三"})

    assert response.status_code == 422
    assert response.json() == {
        "code": "REQUEST_VALIDATION_ERROR",
        "message": "请求参数校验失败",
    }
