"""
当程序遇到不符合预期情况时，可以使用raise语句手动抛出·异常
"""


class AgeError(Exception):
    def __init__(self, msg):
        super().__init__("[年龄异常]:" + msg)


try:
    age = input("输入年龄：")
    if age.isdigit():
        age = int(age)
    else:
        raise ValueError("年龄输入有误")
    if age < 0 or age > 100:
        raise AgeError("年龄过大或过小")  # 自定义异常
except AgeError as e:
    print(e)  # [年龄异常]:年龄过大或过小
except Exception as e:
    print("兜底异常", e)
