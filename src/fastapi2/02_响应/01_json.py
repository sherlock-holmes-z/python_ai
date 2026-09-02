from typing import Generic, TypeVar, Union

import uvicorn
from pydantic import BaseModel, ConfigDict

from fastapi import FastAPI

app = FastAPI()


@app.get("/dict")
async def get():
    return {"hello": "world"}


class Item(BaseModel):
    name: str
    price: float | None = None
    tags: list[str] = []


@app.get("/str")
async def get_str():
    item = Item(name="zhangsan", price=10, tags=["a", "b", "c"])
    return item  # 直接返回,响应类型是个字符串


# response_model设置响应格式为json
# response_model_exclude_unset为True时属性没有值的时候不返回
@app.get("/json", response_model=Item, response_model_exclude_unset=True)
async def get_json():
    item = Item(name="zhangsan", tags=["a", "b", "c"])
    return item


class ErrorResponse(BaseModel):
    code: int
    message: str


# 设置多种响应类型
@app.get("/item_or_else", response_model=Item | ErrorResponse)
async def get_item_or_else(item_name: str | None = None):
    if item_name:
        return Item(name=item_name, price=10, tags=["a", "b"])
    else:
        return ErrorResponse(code=404, message="no item")


# 定义泛型模型
DataT = TypeVar("DataT")


class SuccessResponse(BaseModel, Generic[DataT]):
    # "ignore" 忽略，默认行为
    # "allow" 接收并保留
    # "forbid" 拒绝并报校验错误
    model_config = ConfigDict(extra="forbid")

    code: int = 200
    message: str = "success"
    data: DataT | None = None


# 3.12版本新写法，也可以不用泛型使用Any代替，但那样无法进行pydantic的类型检查
class ErrorResponse[DataT](BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: int = 404
    message: str = "error"
    data: DataT | None = None


# 返回多种响应结果
@app.get("/data_t", response_model=SuccessResponse[Item] | ErrorResponse[str | int])
async def get_data_t(item_name: str | None = None):
    if item_name:
        item = Item(name=item_name, price=10, tags=["a", "b"])
        return SuccessResponse(data=item)
    else:
        return ErrorResponse(data="a")


if __name__ == "__main__":
    uvicorn.run("01_json:app", host="127.0.0.1", port=8000, reload=True)
