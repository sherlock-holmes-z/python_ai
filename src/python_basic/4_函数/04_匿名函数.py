"""
匿名函数是指没有名称的函数，可以简化简单函数的编写
lambda 参数列表: 表达式

函数简单（单行表达式），且只能在一个地方使用，复杂条件下不推荐匿名函数
lambda 一定会返回表达式的计算结果；如果表达式结果为 None，则返回 None
"""

from collections.abc import Callable, Iterable


# 使用匿名函数实现计算效果
def calculate(func, a, b):
    return func(a, b)


print(calculate(lambda a, b: a + b, 1, 2))

# 不推荐这样定义，通常是作为高阶函数的参数进行定义
out_line = lambda: print("--------")  # noqa: E731 - 教学示例：演示匿名函数赋值
out_line()

# 匿名函数典型应用场景，作为高阶函数的参数调用
data_list = ["java ", " python ", "vue", "     c++ "]
data_list.sort(key=lambda a: len(str(a).strip()), reverse=True)
print(data_list)


# 函数中定义函数参数
def process_text(text: str, method) -> str:
    return method(text)


result = process_text(
    "  Python AI  ",
    method=lambda text: text.strip().upper(),
)

print(result)


# 定义一个可以使用lambda的函数
def process_data(data: Iterable[int], method1: Callable[[Iterable[int]], tuple[int, int]]) -> int:
    n1, n2 = method1(data)
    return n1 + n2


result = process_data([1, 2, 3, 4, 5], method1=lambda values: (max(values), min(values)))
print(result)


print("===函数的递归==")


def factorial_recursive(number: int) -> int:
    if number < 0:
        raise ValueError("number 不能为负数")

    if number <= 1:
        return 1

    return number * factorial_recursive(number - 1)


result = factorial_recursive(5)
print(result)
