from fastapi import APIRouter

user_router = APIRouter(prefix="/user", tags=["user路由"])


@user_router.get("/get")
def get_user():
    return {"username": "zhang_san", "age": 23}
