"""
闭包：内层函数inner+被内层函数引用的外部变量__closure__
闭包条件:
    1.要有嵌套函数
    2.【内层函数】要访问【外层函数】的变量
    3.【外层函数】要返回【内层函数】（不返回也有闭包，但只有返回【闭包】才能【存活】）

优点：
    1.可以记住变量状态，不用全局变量，也不用写类，能在多次调用之间保存数据
    2.可以实现‘数据隐藏’，外层变量对外不可见，只能通过内层函数访问
    3.可以做配置过的函数，先传一部分参数把环境固定住，等到一个定制版函数
    4.是装饰器（decorator）等高级用法的基础

缺点：
    1.闭包里引用了很大的对象，又长期不释放，会增加内存占用
    2.很多场景下，【类 + 示例属性】会更清晰，闭包理解成本高，代码难读
"""


def outer():
    global a
    a = 99
    b = 200
    c = 'msg'  # 没有被内层函数使用，__closure__不会包含
    nums = []

    def inner():
        nonlocal b  # 不可变对象修改必须加，修改会改变地址值
        b += 1
        print('inner b:', b)

        # 可变对象修改可以不加nonlocal，不会改变地址值；如果要改变地址值，需要加nonlocal
        nums.append(1)  # 内层函数中用到的变量是可变对象，多个闭包之间互不影响
        print(nums)

    print(inner.__closure__)  # 不返回也有数据
    print('func a:', a)
    return inner


# 每次运行函数都会创建一个新的作用域，运行结束后，局部作用域随之销毁
outer()
outer()
inn = outer()
print('=======', a)

inn()
inn()
# 1.outer函数中，被inner使用到的变量，会被封存到【闭包单元cell】中
# 2.这些cell元素会组成一个__closure__元祖，放到inner函数身上
print(inn.__closure__)  # 获取cell元祖
print(inn.__closure__[0].cell_contents)  # 获取cell元祖中的值

print('======================')
# 调用N次外层函数，就会得到不同的闭包，并且这些闭包之间互不影响
inn_2 = outer()
inn_3 = outer()
inn_2()  # 重新从201打印
inn_3()

print('=========定制版函数========')


def func(char, num):
    def show_msg(msg):
        print(char * num + msg)

    return show_msg


f = func('#', 5)  # 定制函数f,往msg前加五个#
f('lisi')
f2 = func('@@@', 2)
f2('zhangsan')

# 通过类+属性也能实现同样效果
class MyClass:
    def __init__(self,char, num):
        self.num = num
        self.char = char

    def show_msg(self,msg):
        print(self.char * self.num + msg)
cls = MyClass('#', 5)
cls.show_msg('wangwu')
