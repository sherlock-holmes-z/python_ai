import uvicorn
from api.goods import goods_router
from api.user import user_router

from fastapi import FastAPI

fast_api = FastAPI(prefix="/api/v1")

fast_api.include_router(goods_router)
fast_api.include_router(user_router)

if __name__ == "__main__":
    # main       → main.py 模块
    # fast_api   → 模块中的 FastAPI 对象
    uvicorn.run("main:fast_api", host="127.0.0.1", port=8000, reload=True)

    # # reload为true的时候,不能直接传fast_api对象，因为和热加载相违背（新程序无法加载旧对象）
    # uvicorn.run(fast_api, host="127.0.0.1", port=8000, reload=True)
