import uvicorn
from fastapi import FastAPI
from fastapi.params import Path
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/file", response_model=FileResponse)
async def get_file(file_name: str):
    file_path = Path
    return FileResponse(file_name)


if __name__ == '__main__':
    uvicorn.run("03_文件:app", host='127.0.0.1', port=8000, reload=True)
