import os
import time
from threading import RLock, Thread, get_native_id


def inner(lock):
    with lock:
        print(f"inner: pid:{os.getpid()}, thread_id:{get_native_id()}")
        time.sleep(1)


def outer(lock):
    with lock:
        print(f"outer: pid:{os.getpid()}, thread_id:{get_native_id()}")
        time.sleep(2)


if __name__ == "__main__":
    print(f"start: pid:{os.getpid()}, thread_id:{get_native_id()}")
    lock = RLock()  # RLock可重入锁
    t1 = Thread(target=inner, args=(lock,))
    t2 = Thread(target=outer, args=(lock,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(f"end: pid:{os.getpid()}, thread_id:{get_native_id()}")
