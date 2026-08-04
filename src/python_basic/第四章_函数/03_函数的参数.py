"""参数"""

import copy
from collections.abc import Callable

print("======传参方式========")


def method_1(num1, num2, num3) -> None:
    print(num1, num2, num3)


# 位置传参，顺序必须一致（参数少且顺序自然，优先位置传参）
method_1(10, 20, 30)

# 键值对传参，顺序没要求（可读性强，易于扩展，适合参数多的情况）
method_1(num3=33, num2=22, num1=11)

# 位置传参和键值对传参混用,位置传参一定要在关键字参数之前（关键字参数没有顺序要求）
method_1(100, num3=300, num2=200)


print("======默认参数========")


# 默认参数必须放在没有默认值的参数后面
def method_2(name, age, height, sex="男", hobby="lol") -> None:
    print(name, age, height, sex, hobby)


method_2("zhangsan", height=1.80, age=30, hobby="cf")


# 默认参数不能使用可变对象，因为默认参数只会在函数定义时创建一次，后续重复使用会有问题
def add_item(item: int, items: list[int] = []) -> list[int]:
    items.append(item)
    return items


print(add_item(1))  # [1]
print(add_item(2))  # [1, 2]，而不是预期的 [2]
print(add_item(3))  # [1, 2, 3]


# 函数的操作会影响外部传入的可变参数
def add_item2(
    item: int,
    items: list[int] | None = None,  # 可变对象通常使用None作为默认值，再在函数内部创建
) -> list[int]:
    if items is None:
        items = []

    items.append(item)
    return items


# 函数的操作不会影响外部传入的可变参数，函数内使用可变参数副本进行操作
def add_item3(
    item: int,
    items: list[int] | None = None,
) -> list[int]:
    result = [] if items is None else items.copy()  # 如果希望函数不改变传入的列表，copy()或copy.deepcopy(items)
    result.append(item)
    return result


print("=======不定长参数=======")


# 传递的所有匹配位置的参数都会被收集为一个元组
def method_3(*nums) -> None:
    print(sum(nums))


method_3(1, 2, 3, 4)


# k-v关键字传递
def method_4(*nums, **user) -> None:
    print(sum(nums))
    print(user.get("name"), user.get("age"), user.get("hobby"))


method_4(1, 2, name="zhangsan", age=30, hobby="cf")

print("=======函数的参数类型=======")
"""
    普通参数：数字，列表，布尔，字符串，字典，元组，集合
    特殊参数：函数
"""


def add_num(num1: int, num2: int) -> int:
    return num1 + num2


def sub_num(num1: int, num2: int) -> int:
    return num1 - num2


def do_num(num1: int, num2: int, oper) -> int:
    return oper(num1, num2)


print(do_num(1, 2, add_num))

method_5 = add_num  # 函数也可以传递
print("method5:", method_5(1, 2))


# Callable 表示“可调用对象”，包括函数、lambda、实现了 __call__() 的对象、某些类或方法
# Callable[[int, int], int] 表示函数必须接收两个 int，返回一个 int
def do_num2(num1: int, num2: int, oper: Callable[[int, int], int]) -> int:
    return oper(num1, num2)


print(do_num2(2, 3, sub_num))
