"""商品 CRUD 接口。

路由层只处理 HTTP 输入输出和状态码，具体事务、缓存及审计策略统一交给业务服务。
"""

from typing import Annotated

from app.api.dependencies import ProductServiceDep
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from fastapi import APIRouter, Query, Response, status

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, service: ProductServiceDep) -> ProductResponse:
    return await service.create(data)


@router.get("", response_model=list[ProductResponse])
async def list_products(
    service: ProductServiceDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[ProductResponse]:
    return await service.list(offset=offset, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, service: ProductServiceDep) -> ProductResponse:
    return await service.get(product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductServiceDep,
) -> ProductResponse:
    return await service.update(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, service: ProductServiceDep) -> Response:
    await service.delete(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
