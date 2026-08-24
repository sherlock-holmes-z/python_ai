import asyncio
import time


async def work(num):
    print(f"work start:{num}")
    await asyncio.sleep(2)
    print(f"work end:{num}")


async def main():
    print("start")
    start_time = time.time()
    # 虽然是三个协程对象，但是没有生成task,在mainTask中串行执行
    await work(1)
    await work(2)
    await work(3)
    print(f"end:{time.time() - start_time}")


if __name__ == "__main__":
    # 在这一个事件循环中，只有main一个Task
    asyncio.run(main())
