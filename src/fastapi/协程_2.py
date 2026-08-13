"""
协程函数串行执行
"""

import asyncio
import time


async def work(name, dealy):
    print(f"{name} start")
    await asyncio.sleep(dealy)
    print(f"{name} end")


async def main():
    print("============协程函数串行执行耗时==============")
    await work("任务A", 2)  # await串行执行，等到当前函数执行完成后再往下执行
    await work("任务B", 5)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f" executed in {end - start} seconds")
