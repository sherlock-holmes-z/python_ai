# 【上下文管理器】语法格式如下：
#   with 能够调用一个上下文管理器的表达式 as 变量：
#       具体的事1
#       具体的事2
#       具体的事3


# 上下文管理器协议：
#   (1).__enter__ 方法：with 中的代码执行【之前】调用，其返回值会赋值给 as 后的变量。
#   (2).__exit__ 方法：with 中的代码执行【结束后】调用（无论是 with 中否出现异常都会调用）。

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f'say hello:{self.name}, {self.age}')

    def __enter__(self):
        print('开始调用')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('结束调用')
        print(f'异常类型：{exc_type}')
        print(f'异常对象：{exc_val}')
        print(f'异常追踪信息：{exc_tb}')
        return True  # 表示异常已处理，不会抛出
        # return False  # 异常未处理，会往上抛


# 无论with中的代码是正常结束，还是发生异常，都会执行__exit__方法
with Person('lisi', 10) as p:
    p.say_hello()
    p.error_method()
    print('方法即将结束')

# 同时处理多个【上下文管理器0】
with Person('wangwu', 11) as p1, Person('zhaoliu', 12) as p2:
    p1.say_hello()
    p2.say_hello()
