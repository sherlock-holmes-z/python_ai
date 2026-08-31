from typing import Union, Annotated, Optional

from fastapi import FastAPI
from fastapi.params import Query

app = FastAPI()


@app.get("/param")
def param_check(name: str = 'zhangsan', age: int = 18):
    return {"name": name, "age": age}


# 同时允许整型和字符串
# 因为查询参数默认是字符串类型，因此在匹配到类型str后，即使能转成int,也会默认str类型
# 如果希望数字字符串转成整数，可以使用left_to_right从左到右匹配
@app.get("/param2")
def param_check2(item: Annotated[
    Union[int, str],
    Query(union_mode="left_to_right"),
]):
    """数字字符串会转换成数字，此处为借口注释"""
    return {"item": item}


@app.get("/param3")
# def param_check3(item: int | None):
# def param_check3(item: Union[int, None]):
def param_check3(item: Optional[int]):
    """Optional[int] 等同于int | None  等同于 Union[int, None]"""
    return {"item": item}


@app.get("/param_list")
def param_list(items: list):
    return {"items": items}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('04_请求参数类型验证:app', host="127.0.0.1", port=8000, reload=True)
