"""

普通 def 函数
lambda 表达式
内置函数
类
实现了 __call__() 的对象


另外，类型注解本身不会在运行时自动检查参数和返回值，主要供 IDE、mypy、Pyright 等静态检查工具使用。
"""

from collections.abc import Callable


def add(x: int, y: int) -> int:
    return x + y


# 普通函数
operation: Callable[[int, int], int] = add

# lambda表达式
operation2: Callable[[int, int], int] = lambda x, y: x + y


class Add:
    def __call__(self, x: int, y: int) -> int:
        return x + y


# 实现__call__的对象
operation3: Callable[[int, int], int] = Add()
print(operation3(10,20))

class User:
    def __init__(self, name: str):
        self.name = name


# 类，本质是在调用类的构造过程
create_user: Callable[[str], User] = User

user = create_user("张三")
print(user.name)
