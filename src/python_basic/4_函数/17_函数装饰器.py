"""
装饰器：
    1.装饰器是一种可调用对象（通常是函数），它能接受一个函数作为参数，返回一个新函数
    2.可以在不改变原函数代码的情况下，增强或改变原函数的功能

实际应用：
    1.不改变原函数的前提下，统一给函数加上日志，计时，校验，缓存等逻辑
"""


def do_something():
    print("do_something")


def get_func(func):
    def wrapper():  # 这种只适合没有传参的函数，不通用
        print("before")
        func()
        print("after")

    return wrapper


def do_something_2(a, b, c):
    print("do_something_2", a, b, c)


def get_func2(func):
    def wrapper(*args, **kwargs):  # 通用函数
        print("before 2")
        func(*args, **kwargs)
        print("after 2")

    return wrapper


f = get_func(do_something)
f()

f2 = get_func2(do_something_2)
f2(1, 2, {"z": "x"})


# 以上都是手动装饰，需要自己手动获取装饰后的新函数，不推荐
# 推荐直接使用： @装饰器名
def get_func3(func):
    # *args和**kwargs接受参数才能保证函数的兼容性
    def wrapper(*args, **kwargs):
        print("before 3")
        func(*args, **kwargs)
        print("after 3")

    return wrapper


@get_func3
def do_something_3(a, b):
    print("do_something_3", a, b)


# 直接调用函数，就可以有装饰器效果
do_something_3(3, 3)


# 进阶：带参数的装饰器：外层接收配置，中间层接收函数，内存接收具体参数
def get_func4(msg):
    def outer(func):
        def wrapper(*args, **kwargs):
            print(f"{msg}:before 4")
            func(*args, **kwargs)
            print(f"{msg}:after 4")

        return wrapper

    return outer


@get_func4("do_4")  # 带参数
def do_something_4(a, b):
    print("do_something_4", a, b)


@get_func4("do_5")  # 带参数
def do_something_5(a, b):
    print("do_something_5", a, b)


do_something_4(5, {"4": "4"})
do_something_5(5, {"5": "5"})


# 进阶：多个装饰器一起使用
def get_func5(func):
    print("我是装饰器5，开始装饰")

    def wrapper(*args, **kwargs):
        print("wrapper 5")
        return func(*args, **kwargs)

    return wrapper


def get_func6(func):
    print("我是装饰器6，开始装饰")

    def wrapper(*args, **kwargs):
        print("wrapper 6")
        return func(*args, **kwargs)

    return wrapper


# 装饰器先对函数完成装饰，装饰5后对函数装饰，所以先执行我是装饰器6，后执行我是装饰器5
@get_func5
@get_func6
def do_something_6(a, b):
    print("do_something_6", a, b)


# 运行时wrapper从上至下，后装饰的先执行
do_something_6(6, 6)
