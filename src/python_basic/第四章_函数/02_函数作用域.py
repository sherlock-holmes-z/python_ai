"""
全局变量：在函数之外定义的变量，整个文件中都可以使用，通常定义在文件上方
局部变量：在函数内定义的变量，只能函数内使用
"""

num = 100


def method_1() -> None:
    global num  # 使用 global 修饰，num 才能作为全局变量被修改
    num = 200
    print(num)


method_1()
print(num)
