import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# 使用字典接收请求体
@app.post("/user")
def create_user(user: dict):
    user["id"] = 1
    return user


class User(BaseModel):
    name: str
    age: int
    pwd: str | None = None


# 使用类接收请求体
@app.post("/user2")
def create_user2(user: User):
    # user["id"] = 2 模型实例中没有的属性不能添加
    user.pwd = '123456'
    return user


if __name__ == '__main__':
    uvicorn.run('03_post请求体:app', reload=True, port=8000, host="127.0.0.1")
