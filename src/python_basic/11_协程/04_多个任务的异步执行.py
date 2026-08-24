import asyncio
import time


async def work(num):
    print(f"work start:{num}")
    await asyncio.sleep(2)
    print(f"work end:{num}")
    return f"task end:{num}"


async def main():
    print("start")
    start_time = time.time()
    task1 = asyncio.create_task(work(1))
    task2 = asyncio.create_task(work(2))
    task3 = asyncio.create_task(work(3))

    # r1, r2, r3 = await task1, await task2, await task3
    # 等同于asyncio.gather,将多个task提交给事件循环调度，并且在全部执行完后，一次拿到所有结果
    r1, r2, r3 = await asyncio.gather(task1, task2, task3)
    print(r1)
    print(r2)
    print(r3)
    print(f"end:{time.time() - start_time}")


if __name__ == "__main__":
    # 创建事件循环
    asyncio.run(main())
