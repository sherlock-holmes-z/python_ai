# await 的作用：
#
# 1. 等待
#    await 后面必须是可等待对象，例如：协程对象、Task 或 Future。
#
# 2. 可能挂起
#    如果被等待对象暂时无法完成（IO任务），当前任务会在 await 处挂起，
#    并把执行权交还给事件循环。事件循环随后可以运行其他就绪任务。
#
#    如果被等待对象能够立即完成（不包含任何IO操作），await 不一定导致任务挂起或切换。
#
# 3. 恢复
#    被等待对象完成后，当前任务会重新进入可运行状态。
#    当事件循环再次调度该任务时，它会从 await 之后继续执行，
#    await 表达式的结果就是被等待对象的返回值。
#
# 注意：
# - async def 不会自动让普通同步代码变成非阻塞代码。
# - 同步网络请求、同步文件读写和大量 CPU 计算仍会阻塞事件循环。
# - 是否发生任务切换，取决于 await 的对象是否真正产生了挂起。
import asyncio


async def work():
    print("work")
    await asyncio.sleep(2)
    return "work end"


async def main():
    print("main")
    # await 等待一个协程对象执行结束，此时事件循环如果有其他任务，就会切换；没有就阻塞等待
    result = await work()
    print(result)
    return "main end"


if __name__ == "__main__":
    print("start")
    a = asyncio.run(main())
    print(a)
    print("end")
