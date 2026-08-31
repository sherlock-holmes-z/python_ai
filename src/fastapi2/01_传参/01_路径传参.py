import uvicorn
from fastapi import FastAPI

app = FastAPI()


# 请求/args/1前面的会覆盖后面的，只会请求到第一个借口
@app.get("/args/1")
def path_args1():
    return {"hello_1"}


@app.get("/args/{id}")
def path_args2(id):
    return {"hello_2": id}


@app.get("/args/{id}")
def path_args3(id):
    return {"hello_3": id}


# 路径参数默认是字符串类型，可以通过声明类型进行转译
@app.get("/args/{id}/{name}")
def path_args_name(id: int, name):
    return {"hello_4": id, 'name': name}


if __name__ == '__main__':
    uvicorn.run('01_路径传参:app', host="127.0.0.1", port=8000, reload=True)
