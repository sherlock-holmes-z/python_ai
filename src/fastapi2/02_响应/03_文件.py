from collections.abc import Iterator
from pathlib import Path

import uvicorn
from fastapi.responses import FileResponse, StreamingResponse

from fastapi import FastAPI, HTTPException

app = FastAPI()
media_types = {
    "": "application/octet-stream",  # 表示是一个二进制文件
    ".pdf": "application/pdf",
    ".txt": "text/plain; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".csv": "text/csv; charset=utf-8",
    ".json": "application/json",
    ".xml": "application/xml",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
}


# Path("data")获取当前相对路径+/data
# resolve()【相对路径】转成【绝对路径】
FILE_ROOT = Path("data").resolve()


# 直接下载文件（openapi中会返回一个下载地址）
@app.get("/file/{filename}")
async def download_file(filename: str) -> FileResponse:
    file_path = (FILE_ROOT / filename).resolve()

    # 防止使用 ../../ 访问其他目录
    if FILE_ROOT not in file_path.parents:
        raise HTTPException(status_code=400, detail="文件路径不合法")

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        path=file_path,
        # media_type="application/octet-stream",  # octet-stream表示是一个二进制文件
        # media_type="text/plain; charset=utf-8",
        filename=file_path.name,
        # 省略media_type，前提是定义了filename
        # 根据文件扩展名推断 Content-Type,直接使用inline,就会根据文件名自动判断格式预览
        content_disposition_type="inline",
        # content_disposition_type="attachment",# 默认，不预览直接下载,
    )


# 流式下载文件，适合处理大文件
# def iter_file(file_path: Path) -> Iterator[bytes]:
#     with file_path.open("rb") as file:
#         num = 1
#         while chunk := file.read(1024):
#             print(f"read 1.jpg:{num}")
#             num += 1
#             yield chunk


def iter_file(file_path: Path) -> Iterator[bytes]:
    # r读取，b二进制
    with open(file_path, "rb") as f:
        while chunk := f.read(1024):
            yield chunk


# response_class,因为StreamingResponse不是继承了BaseModel的
@app.get("/stream-file")
async def stream_file() -> StreamingResponse:
    file_path = Path("data/1.jpg")

    return StreamingResponse(
        iter_file(file_path),
        media_type="application/jpg",
        headers={
            "Content-Disposition": 'attachment; filename="1.jpg"',
        },
    )


if __name__ == "__main__":
    uvicorn.run("03_文件:app", host="127.0.0.1", port=8000, reload=True)
