"""通用响应模型，统一分页和错误数据结构，便于前端稳定解析。"""

from pydantic import BaseModel, ConfigDict, Field


class PageResponse[DataT](BaseModel):
    """数据库分页结果，而不是把全部记录加载到内存后切片。"""

    model_config = ConfigDict(extra="forbid")

    items: list[DataT]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    pages: int = Field(ge=0)


class ErrorResponse(BaseModel):
    """业务异常的统一响应格式。"""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str


class HealthResponse(BaseModel):
    """健康检查响应；database 为 up 代表实际执行过数据库探测。"""

    status: str
    database: str
