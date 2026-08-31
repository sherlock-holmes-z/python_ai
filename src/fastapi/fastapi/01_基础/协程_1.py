"""
协程函数执行机制：通过await和async关键字实现
协程函数需要有单独的对象来负责执行：EventLoop
协程函数本身不能被直接调用
"""

import asyncio
import time


# 这是一个协程函数
async def hello(name):
    print(f"{name} start")

    # 线程级休眠，阻塞线程
    # time.sleep(1)

    # await 关键字只能在协程函数内部使用
    await asyncio.sleep(5)  # 模拟I/O操作，协程休眠，不会阻塞线程
    print(f"{name} end")


if __name__ == "__main__":
    # 调用 hello() 不会立即执行，只会返回一个协程对象
    coro_obj = hello("1")
    print(type(coro_obj))  # 输出: <class 'coroutine'>
    asyncio.run(coro_obj)  # 启动事件循环，执行携程函数
