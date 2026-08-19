import os
import time
from multiprocessing import Process, current_process

# 这里会执行三次，主进程+两个子进程
print("加载执行")


def run():
    for i in range(10):
        print(f"run:{i}, pid={os.getpid()}")
        time.sleep(2)


def fly():
    for i in range(5):
        print(f"fly:{i}, pid={os.getpid()}")
        time.sleep(3)


def say_hello(a, b, name: str = "no_name"):
    print(f"{current_process().name} - say_hello,{name}:{a},{b}")


# 必须在main方法中运行
# 因为当创建创建子进程时，python不会直接把父进程里的函数交给子进程
# 而是启动一个新的解释器，重新加载一次.py文件,重新加载的函数交给子进程
if __name__ == "__main__":
    # p1和p2在创建时要指定执行的任务
    p1 = Process(target=run)
    p2 = Process(target=fly)

    # 执行进程
    p1.start()
    p2.start()

    # 参数:	作用
    # group:	保留参数，必须始终是 None，不用管它。
    # target:	子进程要执行的函数。传函数本身，不要加括号。
    # name:	进程名称，便于日志和排查。
    # args:	传给 target 的位置参数，必须是元组。
    # kwargs:	传给 target 的关键字参数，必须是字典。
    # daemon:	是否为守护进程。
    p3 = Process(target=say_hello, name="fly_process", args=(1, 2), kwargs={"name": "zhangsan"})
    p3.start()  # 进程的传参args和kwargs必须与函数的入参一致，不能传函数入参不存在的参数
    print(p3.name)
