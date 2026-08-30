"""商品 API 数据模型。

在系统边界完成输入校验，金额使用 Decimal 避免浮点误差，并区分创建、局部更新和响应语义。
"""

from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProductBase(BaseModel):
    """Fields shared by product creation and responses."""

    sku: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    stock: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    """Request body for creating a product."""


class ProductUpdate(BaseModel):
    """Partial update body; omitted fields remain unchanged."""

    sku: str | None = Field(default=None, min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    price: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_patch_fields(self) -> Self:
        """Reject empty patches and nulls for non-nullable database columns."""

        if not self.model_fields_set:
            raise ValueError("至少提供一个需要修改的字段")

        non_nullable_fields = self.model_fields_set - {"description"}
        if any(getattr(self, field_name) is None for field_name in non_nullable_fields):
            raise ValueError("sku、name、price、stock 不能设置为 null")
        return self


class ProductResponse(ProductBase):
    """Public product representation returned by the API and Redis cache."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
