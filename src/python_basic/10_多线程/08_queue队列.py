"""
先进先出，可以跨进程
    如果队列满了，继续put,就会进入等待模式，等别人调用get取走一个元素才能继续put
"""
# 这两个队列方法都是一行的，区别就是multiprocessing的可以跨进程
# from queue import Queue
import time
from multiprocessing import Process, Queue

# 创建队列,不限制大小
q1 = Queue()
q1.empty()
q1.full()
# 如果队列满了，继续put,就会进入等待模式，等别人调用get取走一个元素才能继续put
q1.put(1)

# 队列满了，阻塞等待时间，之后还是满的就抛异常Full
q1.put(2, timeout=5)

# 效果相同，满了直接抛异常
q1.put(3, block=False)
q1.put_nowait(4)

# 同put效果
q1.get()
q1.get(timeout=10)
q1.get(block=False)
q1.get_nowait()


def put_queue(q):
    for i in range(10):
        if not q.full():
            q.put(i)
        else:
            print("满了")
            time.sleep(1)


def get_queue(q):
    while True:
        if not q.empty():
            print(q.get())
        else:
            print("空了")
            time.sleep(1)


if __name__ == "__main__":
    q1 = Queue(5)
    Process(target=put_queue, args=(q1,)).start()
    Process(target=get_queue, args=(q1,)).start()
