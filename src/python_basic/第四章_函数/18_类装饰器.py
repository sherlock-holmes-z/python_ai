"""
类装饰器：
1.一个类有call方法，就可以像调用函数一样调用这个类
2.call方法接收一个函数，返回一个新的函数，name这个类就可以作为类装饰器
"""

print("==========1.手动类装饰器=============")


class SayHello1:
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("Hello")
            func(*args, **kwargs)

        return wrapper


def add1(a, b):
    print("add1:", a + b)


s1 = SayHello1()
add1 = s1(add1)
add1(1, 2)


print("======带参数的类装饰器===========")


class SayHello2:
    name = ""

    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("Hello2")
            func(*args, **kwargs)
            print(self.name)

        return wrapper


def add2(a, b):
    print("add1:", a + b)


s2 = SayHello2("say2")
add2 = s2(add2)
add2(2, 3)


# 通过@语法糖使用类装饰器
@SayHello2("say3")
@SayHello1()  # 要加括号，才能表示这是个函数
def add3(a, b):
    print("add3:", a + b)


add3(3, 4)
