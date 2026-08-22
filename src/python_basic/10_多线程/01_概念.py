"""
并发：一个cpu同时执行多个任务，在多个任务之间高频切换，接近‘同时执行’
并行：同一时刻，每个cpu执行不同任务

"""

import os

print(f"当前电脑cpu逻辑核心数：{os.cpu_count()}")

print(f"当前进程pid={os.getpid()}")
print(f"当前进程父进程pid={os.getppid()}")
