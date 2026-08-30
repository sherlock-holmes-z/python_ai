"""MySQL 商品仓储。

这里只负责商品数据读写，不处理 HTTP、缓存或审计，从而保持单一职责并便于独立测试。
"""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mysql import Product
from app.schemas.product import ProductCreate


class ProductRepository:
    """Encapsulate SQLAlchemy statements for product master data."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.session.add(product)
        await self.session.flush()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.session.get(Product, product_id)

    async def list(self, *, offset: int, limit: int) -> list[Product]:
        statement = select(Product).order_by(Product.id).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def update(self, product: Product, changes: dict[str, Any]) -> Product:
        for field_name, value in changes.items():
            setattr(product, field_name, value)

        await self.session.flush()
        await self.session.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.flush()
