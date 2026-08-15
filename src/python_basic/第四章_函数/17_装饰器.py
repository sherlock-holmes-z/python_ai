"""
装饰器：
    1.装饰器是一种可调用对象（通常是函数），它能接受一个函数作为参数，返回一个新函数
    2.可以在不改变原函数代码的情况下，增强或改变原函数的功能
"""


def do_something():
    print('do_something')


def get_func(func):
    def wrapper():  # 这种只适合没有传参的函数，不通用
        print('before')
        func()
        print('after')

    return wrapper


def do_something_2(a, b, c):
    print('do_something_2', a, b, c)


def get_func2(func):
    def wrapper(*args, **kwargs):  # 通用函数
        print('before 2')
        func(*args, **kwargs)
        print('after 2')

    return wrapper


f = get_func(do_something)
f()

f2 = get_func2(do_something_2)
f2(1, 2, {'z': 'x'})


# 以上都是手动装饰，需要自己手动获取装饰后的新函数，不推荐
# 推荐直接使用： @装饰器名
def get_func3(func):
    # *args和**kwargs接受参数才能保证函数的兼容性
    def wrapper(*args, **kwargs):
        print('before 3')
        func(*args, **kwargs)
        print('after 3')

    return wrapper


@get_func3
def do_something_3(a, b):
    print('do_something_3', a, b)


# 直接调用函数，就可以有装饰器效果
do_something_3(3, 3)
