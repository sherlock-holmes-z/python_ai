import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, get_native_id


def inner(lock):
    with lock:
        print(f"inner: thread_id:{get_native_id()},{threading.current_thread().name}")
        time.sleep(1)
    return "inner"


def outer(lock):
    with lock:
        print(f"outer: thread_id:{get_native_id()},{threading.current_thread().name}")
        time.sleep(2)
    return "outer"


if __name__ == "__main__":
    lock = Lock()
    print("start")
    threadPool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="Thread")
    threadPool.submit(inner, lock)
    threadPool.submit(outer, lock)
    threadPool.shutdown(wait=True)
    print("========end=========")

    # 和进程池类似
    threadPool_2 = ThreadPoolExecutor(max_workers=2, thread_name_prefix="Thread")
    f1 = threadPool_2.submit(inner, lock)
    f2 = threadPool_2.submit(outer, lock)
    threadPool_2.shutdown(wait=True)
    print(f1.result())
    print(f2.result())
    print("========end=========")

    # 按执行结束顺序打印
    threadPool_3 = ThreadPoolExecutor(max_workers=2, thread_name_prefix="Thread")
    futures = [threadPool_3.submit(inner, lock) for _ in range(10)]
    results = []
    for f in as_completed(futures):
        results.append(f.result())
    threadPool_3.shutdown(wait=True)
    print(results)
    print("========end=========")

    # add_done_callback,可以为任务添加回调函数

    # 使用map方法批量提交任务
    # map方法不是阻塞的，但遍历结果是阻塞的,同时map获取任务结果result的顺序，与提交任务的顺序是一样的

    # with 线程池自动调用shutdown自动回收
