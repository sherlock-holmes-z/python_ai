import asyncio


# 这是一个协程函数
async def hello(name):
    print(f"{name} start")
    # await 关键字只能在协程函数内部使用
    await asyncio.sleep(5)  # 模拟I/O操作
    print(f"{name} end")


async def hello2():
    # 执行另一个协程函数,一定要await
    await hello('hello2')


async def main():
    await asyncio.gather(hello('A'), hello('B'))

    c = asyncio.create_task(hello('C'))
    d = asyncio.create_task(hello('D'))
    # 此处可以继续做其他异步工作
    await c
    print('do other Things')
    await d


if __name__ == '__main__':
    # 调用 hello() 不会立即执行，只会返回一个协程对象
    coro_obj = hello('1')
    print(type(coro_obj))  # 输出: <class 'coroutine'>

    # 启动事件循环，执行携程函数
    asyncio.run(coro_obj)
    asyncio.run(hello2())

    asyncio.run(main())
