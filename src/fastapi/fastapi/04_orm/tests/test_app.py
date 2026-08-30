"""应用组装测试。

通过检查 OpenAPI 验证路由已正确注册，并刻意不访问外部服务，使基础测试在任意电脑上都能稳定执行。
"""

from app.main import app


def test_openapi_contains_expected_routes() -> None:
    schema = app.openapi()

    assert "/health" in schema["paths"]
    assert "/api/v1/products" in schema["paths"]
    assert "/api/v1/products/{product_id}" in schema["paths"]
