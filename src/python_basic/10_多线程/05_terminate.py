import time
from multiprocessing import Lock, Process


def run(process_lock):
    try:
        for i in range(3):
            process_lock.acquire()
            print(1, end="")
            print(2, end="")
            print(3)
            time.sleep(3)
            process_lock.release()
    finally:
        # terminate终止的进程不会执行finally，在持有锁是被终止，锁不会释放
        print("run方法执行结束finally")


def fly(process_lock):
    for i in range(3):
        with process_lock:
            print("A", end="")
            print("B", end="")
            print("C")
            time.sleep(3)


if __name__ == "__main__":
    print("主进程start")
    lock = Lock()
    p1 = Process(target=run, args=(lock,))
    p2 = Process(target=fly, args=(lock,))
    p1.start()
    p2.start()

    time.sleep(7)
    print("主进程准备终止p1..")
    p1.terminate()  # 向操作系统申请终止进程
    p1.join()  # join可以等待子进程终止完成，不加join后面直接调用is_alive可能为Ture
    print(p1.is_alive())
    print("主进程end")
