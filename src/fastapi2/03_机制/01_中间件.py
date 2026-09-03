import asyncio

import time

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


# 全局日志、跨域、请求耗时、请求 ID
# 多个中间件，按顺序类似于Aop包裹
@app.middleware("http")
async def add_headers(request: Request, call_next):
    strat_time = time.perf_counter()
    res = await call_next(request)
    # 请求头中增加响应时间
    res.headers["X-Time"] = str(time.perf_counter() - strat_time)
    print('已添加响应时间')
    return res


@app.middleware("http")
async def add_log(request: Request, call_next):
    print(f'请求日志')
    res = await call_next(request)
    print(f'响应日志')
    return res


@app.get("/get_info")
async def get_info():
    await asyncio.sleep(2)
    return {'code': 200}


if __name__ == '__main__':
    uvicorn.run('01_中间件:app', host="127.0.0.1", port=8000, reload=True)
