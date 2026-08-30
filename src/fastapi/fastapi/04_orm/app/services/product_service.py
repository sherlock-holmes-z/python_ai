"""商品业务用例服务。

这里统一编排 MySQL 事务、Redis Cache Aside 和 PostgreSQL 审计；审计采用尽力而为，明确不伪装成跨库强事务。
"""

import logging
from typing import Any

from pydantic import ValidationError
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import DuplicateSkuError, ProductNotFoundError
from app.repositories.audit_repository import ProductAuditRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

logger = logging.getLogger(__name__)


class ProductService:
    """Implement product CRUD with cache-aside reads and best-effort audit."""

    def __init__(
        self,
        *,
        mysql_session: AsyncSession,
        postgresql_session: AsyncSession,
        redis: Redis,
    ) -> None:
        self.mysql_session = mysql_session
        self.postgresql_session = postgresql_session
        self.redis = redis
        self.product_repository = ProductRepository(mysql_session)
        self.audit_repository = ProductAuditRepository(postgresql_session)
        self.cache_ttl_seconds = get_settings().cache_ttl_seconds

    async def create(self, data: ProductCreate) -> ProductResponse:
        try:
            async with self.mysql_session.begin():
                product = await self.product_repository.create(data)
        except IntegrityError as exc:
            raise DuplicateSkuError(data.sku) from exc

        response = ProductResponse.model_validate(product)
        await self._delete_cache(response.id)
        await self._write_audit(
            product_id=response.id,
            action="created",
            payload={"product": response.model_dump(mode="json")},
        )
        return response

    async def get(self, product_id: int) -> ProductResponse:
        cached_product = await self._get_cache(product_id)
        if cached_product is not None:
            return cached_product

        product = await self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)

        response = ProductResponse.model_validate(product)
        await self._set_cache(response)
        return response

    async def list(self, *, offset: int, limit: int) -> list[ProductResponse]:
        products = await self.product_repository.list(offset=offset, limit=limit)
        return [ProductResponse.model_validate(product) for product in products]

    async def update(self, product_id: int, data: ProductUpdate) -> ProductResponse:
        changes = data.model_dump(exclude_unset=True)

        try:
            async with self.mysql_session.begin():
                product = await self.product_repository.get_by_id(product_id)
                if product is None:
                    raise ProductNotFoundError(product_id)
                product = await self.product_repository.update(product, changes)
        except IntegrityError as exc:
            duplicate_sku = str(changes.get("sku", "unknown"))
            raise DuplicateSkuError(duplicate_sku) from exc

        response = ProductResponse.model_validate(product)
        await self._delete_cache(product_id)
        await self._write_audit(
            product_id=product_id,
            action="updated",
            payload={
                "changes": data.model_dump(mode="json", exclude_unset=True),
                "product": response.model_dump(mode="json"),
            },
        )
        return response

    async def delete(self, product_id: int) -> None:
        async with self.mysql_session.begin():
            product = await self.product_repository.get_by_id(product_id)
            if product is None:
                raise ProductNotFoundError(product_id)

            deleted_product = ProductResponse.model_validate(product)
            await self.product_repository.delete(product)

        await self._delete_cache(product_id)
        await self._write_audit(
            product_id=product_id,
            action="deleted",
            payload={"product": deleted_product.model_dump(mode="json")},
        )

    @staticmethod
    def _cache_key(product_id: int) -> str:
        return f"fastapi_orm:product:{product_id}"

    async def _get_cache(self, product_id: int) -> ProductResponse | None:
        cache_key = self._cache_key(product_id)
        try:
            cached_value = await self.redis.get(cache_key)
            if cached_value is None:
                return None
            return ProductResponse.model_validate_json(cached_value)
        except ValidationError:
            logger.warning("删除无法解析的商品缓存 key=%s", cache_key, exc_info=True)
            await self._delete_cache(product_id)
            return None
        except RedisError:
            logger.warning("读取 Redis 商品缓存失败 key=%s", cache_key, exc_info=True)
            return None

    async def _set_cache(self, product: ProductResponse) -> None:
        cache_key = self._cache_key(product.id)
        try:
            await self.redis.set(
                cache_key,
                product.model_dump_json(),
                ex=self.cache_ttl_seconds,
            )
        except RedisError:
            logger.warning("写入 Redis 商品缓存失败 key=%s", cache_key, exc_info=True)

    async def _delete_cache(self, product_id: int) -> None:
        cache_key = self._cache_key(product_id)
        try:
            await self.redis.delete(cache_key)
        except RedisError:
            logger.warning("删除 Redis 商品缓存失败 key=%s", cache_key, exc_info=True)

    async def _write_audit(
        self,
        *,
        product_id: int,
        action: str,
        payload: dict[str, Any],
    ) -> None:
        """Write audit without rolling back an already committed MySQL change."""

        try:
            async with self.postgresql_session.begin():
                await self.audit_repository.create(
                    product_id=product_id,
                    action=action,
                    payload=payload,
                )
        except SQLAlchemyError:
            logger.exception(
                "写入 PostgreSQL 审计失败 product_id=%s action=%s",
                product_id,
                action,
            )
