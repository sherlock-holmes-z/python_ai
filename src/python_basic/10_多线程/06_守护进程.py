import os
import time
from multiprocessing import Process
from multiprocessing.process import current_process


def read_line():
    while True:
        # 不写model默认读取文本
        with open("file/1.txt", encoding="utf-8") as f:
            process = current_process()
            sum_lines = sum(1 for _ in f)  # 大文件读取，读一行计数一次，不会将文件内容全部加载到内存中
            print(f"{process.name}读取:{sum_lines}")
            time.sleep(1)


def normal_function():
    while True:
        process = current_process()
        print(f"{process.name}")
        time.sleep(1)


if __name__ == "__main__":
    # 守护进程中，不允许再创建新的子进程
    # 守护进程的设置必须在start之前，启动不不能再将子进程设置为守护进程
    p1 = Process(name="守护进程", target=read_line, daemon=True)
    p1.start()

    p2 = Process(name="normal", target=normal_function)
    p2.start()

    print("主进程start")
    with open("file/1.txt", mode="a", encoding="utf-8") as f:
        for i in range(5):
            f.write("hello world\n")
            f.flush()  # 写一次就刷一次盘
            time.sleep(1)
    print("主进程end")  # 主进程结束，自动销毁守护进程p1,但是子进程p2不会结束
