import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[  # 允许的域名
        "http://localhost:63342",
        "https://www.example.com",
    ],
    allow_credentials=True,  # 允许携带cookie
    allow_methods=[  # 允许的请求方法
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[  # 允许的请求头
        "Authorization",
        "Content-Type",
    ],
)


@app.get('/')
async def get_info():
    return {'hello': 'world'}


# CORS跨域
if __name__ == '__main__':
    uvicorn.run('02_跨域资源共享:app', host='127.0.0.1', port=8000, reload=True)
