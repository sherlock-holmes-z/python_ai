import time
from multiprocessing import Lock, Process


def run(process_lock):
    for i in range(10):
        process_lock.acquire()
        print(1, end='')
        print(2, end='')
        print(3, end='')
        print(4, end='')
        print(5)
        time.sleep(3)
        # 如果程序中间抛出异常，锁就会无法释放
        # 前面上几次锁，就要释放几次
        process_lock.release()


def fly(process_lock):
    for i in range(10):
        # 进入时自动枷锁，结束时自动解锁
        with process_lock:
            print('A', end='')
            print('B', end='')
            print('C', end='')
            print('D', end='')
            print('E')
            time.sleep(3)


if __name__ == "__main__":
    print('主进程start')
    lock = Lock()
    p1 = Process(target=run, args=(lock,))
    p2 = Process(target=fly, args=(lock,))
    p1.start()
    p2.start()
    print('主进程end')
