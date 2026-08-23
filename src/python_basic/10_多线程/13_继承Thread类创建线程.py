import os
import time
from threading import Lock, Thread, get_native_id


class InnerThread(Thread):
    def __init__(self, lock, **kwargs):
        super().__init__(**kwargs)
        self.lock = lock

    def run(self):
        with self.lock:
            print(f"inner: pid:{os.getpid()}, thread_id:{get_native_id()},{self.name}")
            time.sleep(2)


class OuterThread(Thread):
    def __init__(self, lock, **kwargs):
        super().__init__(**kwargs)
        self.lock = lock

    def run(self):
        with self.lock:
            print(f"outer: pid:{os.getpid()}, thread_id:{get_native_id()},{self.name}")
            time.sleep(2)


if __name__ == "__main__":
    print("start")
    lock = Lock()
    inner = InnerThread(lock, name="inner", daemon=False)  # 线程名直接通过实现线程Thread的类对象self.name即可获取
    outer = OuterThread(lock, name="outer")
    inner.start()
    outer.start()
    inner.join()
    outer.join()
    print("end")
