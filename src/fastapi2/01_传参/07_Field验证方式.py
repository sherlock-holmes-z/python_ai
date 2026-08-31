from enum import StrEnum

import uvicorn
from pydantic import BaseModel, Field

from fastapi import FastAPI

app = FastAPI()


class GenderEnum(StrEnum):
    male = "male"
    female = "female"


class User(BaseModel):
    name: str = Field(min_length=2, max_length=4)
    age: int
    # age: int = Field(...) # 显示申明必填，和上面的效果一样
    gender: GenderEnum = Field(default=GenderEnum.male)


@app.post("/user")
async def create_user(user: User):
    return user


class Item(BaseModel):
    # 给openapi文档中字段增加书名和例子
    name: str = Field(min_length=1, max_length=100, title="商品名称", description="简介", examples=["手机", "电脑"])


@app.post("/item")
async def create_item(item: Item):
    return item


if __name__ == "__main__":
    uvicorn.run("07_Field验证方式:app", host="127.0.0.1", port=8000, reload=True)
