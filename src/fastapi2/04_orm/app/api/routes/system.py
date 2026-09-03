"""系统接口：提供不包含业务数据的数据库健康探测。"""

from fastapi import APIRouter
from sqlalchemy import text

from app.api.dependencies import SessionDep
from app.schemas.common import HealthResponse

router = APIRouter(tags=["系统"])


@router.get("/health", response_model=HealthResponse)
async def health_check(session: SessionDep) -> HealthResponse:
    """执行 SELECT 1，区分 Web 进程存活和数据库真正可用。"""

    await session.execute(text("SELECT 1"))
    return HealthResponse(status="ok", database="up")
