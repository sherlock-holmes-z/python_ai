"""领域异常定义。

业务层抛出与框架无关的异常，再由应用边界转换成 HTTP 响应，避免业务代码耦合 FastAPI。
"""


class ProductNotFoundError(Exception):
    """Raised when a requested product does not exist."""

    def __init__(self, product_id: int) -> None:
        self.product_id = product_id
        super().__init__(f"商品不存在: {product_id}")


class DuplicateSkuError(Exception):
    """Raised when a product SKU violates the unique constraint."""

    def __init__(self, sku: str) -> None:
        self.sku = sku
        super().__init__(f"商品 SKU 已存在: {sku}")
