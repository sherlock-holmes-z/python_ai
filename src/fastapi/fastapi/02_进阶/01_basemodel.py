import uvicorn
from pydantic import BaseModel, EmailStr, Field

from fastapi import FastAPI, Query


class User(BaseModel):
    name: str = "无名氏"
    age: int = Field(default=1, ge=1, le=150)  # ge le大于等于，小于等于，gt lt大于小于·
    email: EmailStr | None = None

    def __str__(self) -> str:
        return f"{self.name} {self.age} {self.email}"


class NewUser(BaseModel):
    name: str
    age: int
    height: float


app = FastAPI()


# Query → 管 URL 后面 ? 带的参数，用在函数参数上
# Field → 管 请求体 JSON 里的字段，用在 Pydantic 模型上
@app.post("/user")
def get_user(user: User, desc: str = Query(default="用户", min_length=1, max_length=2)):
    # return str(user)
    print(desc)
    return user.model_dump()  # 将user对象直接转json输出


# response对象中的属性如果没有设置默认值，就代表必输出，否则报错
@app.post("/user_response", response_model=NewUser)
def get_user_response(user: User):
    print(user)
    return NewUser(name=user.name, age=user.age)


if __name__ == "__main__":
    uvicorn.run("01_basemodel:app", host="127.0.0.1", reload=True, port=8000)
