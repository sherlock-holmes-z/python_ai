"""
fastapi运行：
uvicorn src.fastapi.fastapi.01_fast:app --reload
uvicorn是ASGI服务器，负责请求并调用fastapi应用


FastAPI 底层维护了一个类似于字典的APIRoute对象
键 K：请求路径 + HTTP 方法
值 V：路由处理函数
当请求发送给 uvicorn 服务器，将根据请求路径（键）找到对应的值（函数）进行调用，并且返回结果。

"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/demo2/{msg}")
def demo2(msg: str):
    return {"message": msg}


@app.get("/demo3/{msg}")
def demo3(msg: int):
    return {"message": msg}
