import time
from multiprocessing import Lock, Process


def run(process_lock):
    for i in range(3):
        process_lock.acquire()
        print(1, end="")
        print(2, end="")
        print(3)
        time.sleep(3)

        process_lock.release()


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
    p1.join(5)  # 表示等多久再往下执行，单位秒
    p2.start()

    # 主进程等待子进程执行完成后再往下执行
    p1.join()
    p2.join()
    print("主进程end")
