"""
文件上传不能与json请求混用，只能与form表单请求一起使用
"""

from typing import Annotated

import aiofiles
import uvicorn
from fastapi.params import Form
from pydantic import WithJsonSchema

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


# 小文件上传:将整个文件加载进内存，二进制上传
@app.post("/upload")
def upload(file_bytes: bytes = File(...)):
    # wb 二进制写入
    with open("data/1.jpg", "wb") as f:
        f.write(file_bytes)
    return "upload success"


@app.post("/upload_big")
async def upload_big(file: UploadFile = File(...)):
    # async with 代码块结束后异步关闭文件
    # aiofiles.open异步打开磁盘文件，避免进入阻塞，wb二进制写入
    async with aiofiles.open("data/2.jpg", "wb") as output:
        # while True:
        #     chunk = await file.read(1024)
        #     if not chunk:
        #         break
        #     await output.write(chunk)

        # 上方代码等同于，chunk在循环条件中复制
        while chunk := await file.read(1024):
            print("正在写入。。。")
            await output.write(chunk)
    return "upload success"


# 解决fastapi与swagger-ui的兼容问题
BinaryUploadFile = Annotated[
    UploadFile,
    WithJsonSchema(
        {
            "type": "string",
            "format": "binary",
        }
    ),
]


@app.post("/upload_batch")
def upload_batch(file_list: Annotated[list[BinaryUploadFile], File(...)]):
    return {"names": [f.filename for f in file_list]}


# 同时上传文件和表单数据（文件只能和表单数据一起提交，不能和json一起）
@app.post("/upload_new_file")
def upload_new_file(file: Annotated[BinaryUploadFile, File(...)], new_file_name: Annotated[str, Form(...)]):
    return {"names": file.filename, "new_file_name": new_file_name}


if __name__ == "__main__":
    uvicorn.run("10_文件上传:app", host="127.0.0.1", port=8000, reload=True)
