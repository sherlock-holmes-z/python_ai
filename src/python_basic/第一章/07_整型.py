import sys

# 当数很大时，可以用下划线将数字分组，使整数易读
num = 1_000_000

# python中整数的上限值，取决于执行代码的计算机的内存和处理能力
a=9 ** 9999

# print最多可以输出4300位，通过sys.set_int_max_str_digits设置0表示不限制
sys.set_int_max_str_digits(0)
print(a)
