import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def work(a):
    print(f"start work:{a},pid:{os.getpid()}")
    if a % 2 == 0:
        time.sleep(1)
    else:
        time.sleep(2)
    return f"end work:{a},pid:{os.getpid()}"


if __name__ == "__main__":
    print("start")
    poolExecutor = ProcessPoolExecutor(max_workers=2)
    # submit只提交任务，不阻塞进程
    f1 = poolExecutor.submit(work, 1)
    f2 = poolExecutor.submit(work, 2)
    f3 = poolExecutor.submit(work, 3)
    f4 = poolExecutor.submit(work, 4)
    f5 = poolExecutor.submit(work, 5)
    f6 = poolExecutor.submit(work, 6)

    # .result()会阻塞主进程，等待子进程任务执行完成获取返回结果后再往下运行
    print(f1.result(), f2.result(), f3.result(), f4.result(), f5.result(), f6.result())

    # shutdown表示不再接受新的任务
    # wait=True：阻塞主进程，等待进程池中所有任务执行完毕
    poolExecutor.shutdown(wait=True)
    print("======end")

    # 批量提交进程
    poolExecutor_2 = ProcessPoolExecutor(max_workers=2)
    futures = [poolExecutor_2.submit(work, a) for a in range(5)]
    poolExecutor_2.shutdown(wait=True)
    for f in futures:
        print(f.result())
    print("======end")

    print("as_completed：按执行结束顺序")
    poolExecutor_3 = ProcessPoolExecutor(max_workers=3)
    futures = [poolExecutor_3.submit(work, a) for a in range(3)]
    # 先执行结束的先打印(as_completed不能放在shutdown后使用，那样所有进程都已经执行结束了)
    for f in as_completed(futures):
        print(f.result())

    poolExecutor_3.shutdown(wait=True)
    print("======end")

    # 为任务添加回调函数
    print("add_done_callback 指定回调函数")

    def callback(future):
        print(f"callback:{future.result()}")

    poolExecutor_4 = ProcessPoolExecutor(max_workers=3)
    futures = [poolExecutor_4.submit(work, a) for a in range(3)]
    for f in futures:
        f.add_done_callback(callback)
    poolExecutor_4.shutdown(wait=True)
    print("======end")

    print("map 批量提交任务")

    poolExecutor_5 = ProcessPoolExecutor(max_workers=3)

    # 通过map批量提交进程任务，返回的是一个生成器，
    results = poolExecutor_5.map(work, range(5))

    # 获取生成器中的内容，生成器转list会等待任务全部执行完成，按任务提交顺序
    print(list(results))
    poolExecutor_5.shutdown(wait=True)
    # for r in results:
    #     print(r)
    print("======end")

    # 离开with代码块，进程池自动shutdown(wait=True)
    with ProcessPoolExecutor(max_workers=3) as executor:
        print("with")
        futures = [executor.submit(work, a) for a in range(5)]
    for f in futures:
        print(f.result())
