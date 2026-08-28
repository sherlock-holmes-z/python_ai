from urllib.request import Request

import uvicorn

from fastapi import FastAPI

app = FastAPI()


# 全局接口统一处理：app中所有的接口都被包裹
# 多个中间件，从上至下包裹，类似aop
@app.middleware("http")
async def middleware(request: Request, call_next):
    print("start1")
    response = await call_next(request)  # 发起请求
    print("end1")
    return response


@app.middleware("http")
async def middleware_2(request: Request, call_next):
    print("start2")
    response = await call_next(request)
    print("end2")
    return response


@app.get("/")
async def get():
    return "test"


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="127.0.0.1")
