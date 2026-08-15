"""
    局部作用域：            函数内部的变量，只在当前函数有效
    嵌套函数外层作用域：     内嵌函数的外层函数
    全局作用域：            定义在函数外面的变量
    内建作用域：            Python自带的名字，比如print,len

    作用域可以从内至外查找，但是不能从外至内
"""

# a全局作用域
a = 100


def outer():
    global a  # 局部作用域可以访问但不能修改全局变量，加global才能修改
    a = 99
    b = 200

    def inner():
        nonlocal b  # 内层函数可以访问外层函数的变量但不能修改，需加nonlocal
        b += 1
        print('inner b:', b)

    print('func a:', a)
    return inner


# 每次运行函数都会创建一个新的作用域，运行结束后，局部作用域随之销毁
outer()
outer()
inn = outer()
print('=======', a)
inn()
inn()
inn()
