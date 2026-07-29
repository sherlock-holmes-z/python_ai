"""
列表
有序，可变，允许重复，可以放不同类型元素
通过索引（整数）访问。类似数组。用途：通用集合
"""

from typing import Any

score_list = list(range(1, 5))
print(score_list)

score_list[0] = 2  # 可变，允许重复，通过索引访问
print(score_list)

score_list[1] = "strong"  # 可以放不同类型元素, 警告是因为py推断当前是个整数列表，却放了个字符串
print(score_list)

del score_list[1]  # 删除元素
print(score_list)

"""声明任意类型"""
any_list: list[Any] = list(range(1, 11))
any_list[0] = "字符串"
any_list[1] = True
print(any_list)

"""申明字符串和整数类型"""
str_int_list: list[int | str] = list(range(10, 15))
str_int_list[0] = "str_int_list"
print(str_int_list)

"""列表切片"""
new_list = str_int_list[0:4:2]
print(f"new_list{new_list}")

"""常用方法"""
num_list = [3, 1, 2]
print(num_list)

num_list.append(4)  # 末尾追加
print(num_list)

num_list.insert(0, 0)  # 在指定索引处插入
print(num_list)

num_list.extend([5, 6])  # 合并另一个可迭代对象
print(num_list)

num_list.remove(0)  # 删除第一个匹配的元素
print(num_list)

print(num_list.pop())  # 弹出并返回末尾元素
print(num_list)

print(num_list.index(2))  # 查找元素首次出现的索引

num_list.sort()  # 原地升序排序
print(num_list)

num_list.reverse()  # 原地反转
print(num_list)

print(num_list.count(2))  # 统计某元素出现次数

copy_list = num_list.copy()  # 浅拷贝
print(copy_list)

num_list.clear()  # 清空列表
print(num_list)
