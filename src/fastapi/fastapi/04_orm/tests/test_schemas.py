"""商品数据模型校验测试。

测试输入边界和局部更新规则，无需连接数据库即可快速发现 API 契约回归。
"""

from decimal import Decimal

import pytest
from app.schemas.product import ProductCreate, ProductUpdate
from pydantic import ValidationError


def test_product_create_accepts_valid_values() -> None:
    product = ProductCreate(
        sku="BOOK-PYTHON-001",
        name="Python 后端开发",
        price=Decimal("99.00"),
        stock=10,
    )

    assert product.price == Decimal("99.00")
    assert product.stock == 10


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [("price", Decimal("0")), ("stock", -1)],
)
def test_product_create_rejects_invalid_numeric_values(
    field_name: str,
    field_value: Decimal | int,
) -> None:
    data = {
        "sku": "BOOK-PYTHON-001",
        "name": "Python 后端开发",
        "price": Decimal("99.00"),
        "stock": 10,
    }
    data[field_name] = field_value  # type: ignore[assignment]

    with pytest.raises(ValidationError):
        ProductCreate.model_validate(data)


def test_product_update_rejects_empty_patch() -> None:
    with pytest.raises(ValidationError, match="至少提供一个"):
        ProductUpdate()


def test_product_update_allows_clearing_description() -> None:
    update = ProductUpdate(description=None)

    assert update.model_dump(exclude_unset=True) == {"description": None}
