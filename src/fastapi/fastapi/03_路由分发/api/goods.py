from fastapi import APIRouter

goods_router = APIRouter(prefix="/goods", tags=["goods路由"])


@goods_router.get("/get")
def get_goods():
    return {"name": "car", "price": 10}
