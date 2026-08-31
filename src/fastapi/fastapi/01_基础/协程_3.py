"""
协程函数并行执行
需要结合Task以及gather()函数实现
需要将协程任务封装为task对象：通过create_task()函数，一旦任务封装以后协程函数会立即执行
"""

import asyncio
import time


async def work(name, dealy):
    print(f"{name} start")
    await asyncio.sleep(dealy)
    print(f"{name} end")
    return name


async def main():
    print("============协程函数并行执行耗时==============")
    task_a = asyncio.create_task(work("A", 5))
    task_b = asyncio.create_task(work("B", 7))

    #  await 让当前协程等待这组任务完成
    #  asyncio.gather() 把多个任务组合成一个全部完成才结束的等待对象，并按传入顺序收集它们的返回值
    result = await asyncio.gather(task_a, task_b)  # 主线程等待AB执行完毕，并接收返回值
    print('=============任务执行完成，输出返回值===========')
    # 所有任务的返回值都会在一个list里
    print(result)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f" executed in {end - start} seconds")
