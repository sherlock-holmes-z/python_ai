import uvicorn
from fastapi import FastAPI

app = FastAPI()


# 浏览器中直接通过/query?page=1&limit=10传参
# 没有申明默认值，参数为必输
@app.get("/query")
def query_args(page: int, limit: int):
    return {"page": page, "limit": limit}


# 如果需要非必输且不想要默认值，可以默认值设为None，不传返回null
# {
#   "page": 1,
#   "limit": null
# }
@app.get("/query2")
def query_args_2(page: int, limit: int | None = None):
    return {"page": page, "limit": limit}

# 路径参数，查询参数混用
@app.get("/query3/{page}")
def query_args_3(page: int, limit: int):
    return {"路径参数page": page, "查询参数limit": limit}


if __name__ == '__main__':
    uvicorn.run("02_查询参数:app", host="127.0.0.1", port=8000, reload=True)
