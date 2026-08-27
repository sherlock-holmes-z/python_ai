"""
fastapi运行：
uvicorn src.fastapi.fastapi.01_fast:app --reload
uvicorn是ASGI服务器，负责请求并调用fastapi应用


FastAPI 底层维护了一个类似于字典的APIRoute对象
键 K：请求路径 + HTTP 方法
值 V：路由处理函数
当请求发送给 uvicorn 服务器，将根据请求路径（键）找到对应的值（函数）进行调用，并且返回结果。

"""

import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


# 同等级目录下，如果有接收参数和不接收参数的同等级路径
# 不接收参数的路径要在接收参数的路径前，不然会被覆盖
# （比如/demo2/hello和/demo2/{msg}）
@app.get("/demo2/hello")
def demo2_hello():
    return {"message": " demo2 Hello World"}


@app.get("/demo2/{msg}")
def demo2(msg: str):
    return {"message": msg}


@app.get("/demo3/{msg}")
def demo3(msg: int):
    return {"message": msg}


# 根据名字匹配参数,如果没有设置默认值，参数不传就报错
# /demo4?a=1&b=1&c=1
@app.get("/demo4")
def demo4(a, b, c: str = "c"):
    return {"a": a, "b": b, "c": c}


# bool，传1，true,True,on,yes都是true，0是false
@app.get("/demo5")
def demo5(a: bool):
    return {"a": a}


if __name__ == "__main__":
    # reload=true，热部署，文件修改自动更新
    uvicorn.run(app="01_fast:app", host="127.0.0.1", port=8000, reload=True)
