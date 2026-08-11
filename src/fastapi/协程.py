import asyncio


# 这是一个协程函数
async def hello():
    print("Hello")
    # await 关键字只能在协程函数内部使用
    await asyncio.sleep(1)  # 模拟I/O操作
    print("World")


async def hello2():
    print("Hello2")
    # 执行另一个协程函数
    await hello()


if __name__ == '__main__':
    # 调用 hello() 不会立即执行，只会返回一个协程对象
    coro_obj = hello()
    print(type(coro_obj))  # 输出: <class 'coroutine'>

    # 启动事件循环，执行携程函数
    asyncio.run(coro_obj)

    asyncio.run(hello2())
