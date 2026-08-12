"""
函数定义中，*args 把多个位置参数打包成元组。
函数定义中，**kwargs 把多个关键字参数打包成字典。
函数调用中，*列表 / *元组 把序列解包为位置参数。
函数调用中，**字典 把字典解包为关键字参数。
"""


def get_info():
    return 1, 2


def show_info(*args, **kwargs):
    print(args)
    print(kwargs)


if __name__ == '__main__':
    a, b = get_info()
    print(a, b)  # 返回值解包
    print(get_info())  # 返回元祖

    show_info(1, 1, 1, name='zhangsan', age=18)
    show_info([2, 2], name='lisi')  # 位置参数不会自动解包，整个list会被认为是元祖中一个元素
    show_info(*[3, 3], name='lisi')  # 主动解包传入位置参数

    person = {'name': 'lisi', 'age': 18}
    show_info(**person)  # 关键字入参时要解包，不然会被认为是位置参数的一个元祖
