from typing import Annotated

import uvicorn

from fastapi import Depends, FastAPI

app = FastAPI()


def get_message() -> str:
    print("depends")
    return "Hello Depends"


@app.get("/")
def get(message: str = Depends(get_message)):  # 客户端请求会先执行get_message,将结果注入参数message中
    return {"message": message}


# 3.12推荐新写法,【依赖】和【依赖返回类型】同时声明，方便复用
MessageDep = Annotated[str, Depends(get_message)]


@app.get("/get")
def get_message2(message: MessageDep):
    return {"message": message}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
