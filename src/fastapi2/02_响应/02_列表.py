import random
from typing import Annotated, TypeVar, Generic

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    price: float


Data_T = TypeVar('Data_T')


class SuccessResponse(BaseModel, Generic[Data_T]):
    code: int = 200
    msg: str = 'success'
    data: Data_T


Page_Data = TypeVar('Page_Data')


class PageInfo(BaseModel, Generic[Page_Data]):
    total: int
    pages: int
    # default_factory=list每次创建PageInfo都会创建一个新列表
    page_data: list[Page_Data] = Field(default_factory=list)


@app.get("/item_page", response_model=SuccessResponse[PageInfo[Item]])
async def read_items(
    page: Annotated[int, Query(ge=1, description='页码')] = 1,
    page_size: Annotated[int, Query(ge=10, le=100, multiple_of=10, description='条数')] = 10,
    price: Annotated[int, Query(description='大于次价格')] = 0):
    items = [Item(id=i, name=f'item{i}', price=random.randint(1, 100)) for i in range(100)]
    new_items = list(filter(lambda item: item.price > price, items))
    return SuccessResponse(data=PageInfo(total=len(new_items), pages=page, page_data=new_items[:page_size]))


if __name__ == '__main__':
    uvicorn.run('02_列表:app', host="127.0.0.1", port=8000, reload=True)
