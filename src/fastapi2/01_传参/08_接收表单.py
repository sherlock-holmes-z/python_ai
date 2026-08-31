# python -c "import multipart; print(multipart.__version__)" 一般安装fastapi后也会包含multipart
from typing import Annotated

import uvicorn
from pydantic import BaseModel

from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/upload")
def upload(file_name: str = Form(...), desc: str = Form(...)):
    return {"file_name": file_name, "desc": desc}


class FileInfo(BaseModel):
    name: str
    desc: str


# 将class对象以表单的形式传输·
@app.post("/upload_file")
def upload_file(file: Annotated[FileInfo, Form(...)]):
    return {"file_name": file.name, "desc": file.desc}


if __name__ == "__main__":
    uvicorn.run("08_接收表单:app", host="127.0.0.1", port=8000, reload=True)
