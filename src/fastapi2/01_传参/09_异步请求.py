"""
FastAPI 调用的 async def 路由/依赖 → 事件循环
FastAPI 调用的 def 路由/依赖       → 线程池
自己直接调用普通 def               → 当前线程直接执行
"""

import asyncio
import threading
import time

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="同步请求与异步请求示例")


def blocking_task(delay: float) -> tuple[str, str]:
    """模拟无法使用 await 的同步阻塞操作。"""
    time.sleep(delay)
    return "同步任务执行完成", threading.current_thread().name


async def async_task(dealy: float):
    print('async_task start')
    await asyncio.sleep(dealy)
    print('async_task end')


@app.get("/async")
async def async_request(delay: float = 2.0) -> dict[str, str | float]:
    """异步路由：由事件循环执行，等待期间可以处理其他请求。"""
    started_at = time.perf_counter()

    # asyncio.sleep() 是异步等待，会在等待期间让出事件循环。
    # await asyncio.sleep(delay)

    tasks = [async_task(delay) for _ in range(10)]
    await asyncio.gather(*tasks, return_exceptions=True)

    return {
        "request_type": "async",
        "message": "异步请求执行完成",
        "thread": threading.current_thread().name,
        "elapsed_seconds": round(time.perf_counter() - started_at, 2),
    }


@app.get("/sync")
def sync_request(delay: float = 2.0) -> dict[str, str | float]:
    """同步路由：FastAPI 会把普通 def 路由放在线程池中执行。"""
    started_at = time.perf_counter()

    # time.sleep() 会阻塞当前线程，但不会阻塞主事件循环线程。
    message, task_thread = blocking_task(delay)

    return {
        "request_type": "sync",
        "message": message,
        "thread": task_thread,
        "elapsed_seconds": round(time.perf_counter() - started_at, 2),
    }


@app.get("/async/run-sync")
async def async_run_sync(delay: float = 2.0) -> dict[str, str | float]:
    """异步路由调用同步阻塞函数：手动把任务交给线程执行。"""
    started_at = time.perf_counter()

    # 不要直接在 async def 中调用 blocking_task()，否则会阻塞事件循环。
    message, task_thread = await asyncio.to_thread(blocking_task, delay)

    return {
        "request_type": "async-to-thread",
        "message": message,
        "route_thread": threading.current_thread().name,
        "blocking_task_thread": task_thread,
        "elapsed_seconds": round(time.perf_counter() - started_at, 2),
    }


if __name__ == '__main__':
    uvicorn.run('09_异步请求:app', host="127.0.0.1", port=8000, reload=True)
