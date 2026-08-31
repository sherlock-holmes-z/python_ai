"""Query 参数验证示例。

启动后访问 http://127.0.0.1:8000/docs，可直接在 Swagger UI 中测试。
不满足约束时，FastAPI 会自动返回 422 Unprocessable Entity。
"""

from typing import Annotated

import uvicorn

from fastapi import FastAPI, Query

app = FastAPI()


# 1. 必填参数、默认值与可选参数,Query中通过default设置默认值
# /articles?keyword=fastapi
@app.get("/articles")
def list_articles(
    keyword: str,
    page: int = Query(default=1, ge=1, le=100),
    page_size: int | None = None,
):
    return {"keyword": keyword, "page": page, "page_size": page_size}


# 2. 数值范围：ge/gte、gt、le/lte、lt 与 multiple_of必须是10的倍数，Annotated在末尾设置默认值
# /pagination?page=2&page_size=20
@app.get("/pagination")
def pagination(
    page: Annotated[int, Query(ge=1, description="页码，从 1 开始")] = 1,
    page_size: Annotated[
        int,
        Query(ge=10, le=100, multiple_of=10, description="每页数量，10~100 且为 10 的倍数"),
    ] = 10,
):
    return {"page": page, "page_size": page_size}


# 3. 字符串验证：min_length、max_length 与 pattern（正则表达式）
# /users?username=tom_123
@app.get("/users")
def get_user(
    username: Annotated[
        str,
        Query(
            min_length=3,
            max_length=20,
            pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$",  # regex也可以
            description="3~20 位，以字母开头，只能包含字母、数字和下划线",
        ),
    ],
):
    return {"username": username}


# 4. 使用 alias别名：Python 中使用 q，客户端传入参数名 search，客户端传q不会被识别
# /search?search=python
@app.get("/search")
def search(
    q: Annotated[
        str | None,
        Query(alias="search", min_length=1, max_length=50, description="搜索关键词"),
    ] = None,
):
    return {"q": q}


# 5. 同名 Query 参数可以接收为列表
# /products?tag=python&tag=fastapi
@app.get("/products")
def list_products(
    tag: Annotated[
        list[str] | None,
        Query(min_length=1, max_length=5, description="最多传入 5 个 tag 参数"),
    ] = None,
):
    return {"tags": tag}


if __name__ == "__main__":
    uvicorn.run("05_Query请求方式:app", host="127.0.0.1", port=8000, reload=True)
