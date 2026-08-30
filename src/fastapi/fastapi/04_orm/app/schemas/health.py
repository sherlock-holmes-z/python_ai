"""外部依赖健康状态响应模型。

固定响应字段和状态值，既方便监控系统解析，也避免把底层异常详情暴露给调用方。
"""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health state without leaking connection credentials or exceptions."""

    status: Literal["ok", "degraded"]
    dependencies: dict[str, Literal["up", "down"]]
