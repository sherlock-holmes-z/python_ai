"""
协程是一段可以在执行过程中主动暂停，并在之后从暂停位置继续执行的计算过程。
注意：协程不是由操作系统提供的，是程序员在用户态实现的切换机制
"""

import asyncio

# 协程函数：使用async关键字修饰的函数，调用协程函数，会获得协程对象
# 调用协程函数，并不会执行【协程函数】中的代码


async def work():
    print("work")
    return "work end"


if __name__ == "__main__":
    w = work()  # 调用协程函数，返回的是协程对象，此时不会执行协程函数中的代码
    print(w)

    # asyncio.run做了三件事
    # 1.创建事件循环
    # 2.将收到的协程对象包装成一个任务Task,交给事件循环
    # 3.启动事件循环
    # ！！！注意：asyncio.run会阻塞当前线程，直到任务执行完毕，并返回任务的执行结果
    result = asyncio.run(w)
    print(result)
