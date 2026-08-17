"""
将一组数据不停合并，最终归并成一个结果
语法格式：reduce(合并函数，可迭代对象，初始值)

注：reduce需要从functools中引入才能使用
"""

from functools import reduce

# 数值统计
nums = [1, 2, 3, 4, 5]
sum_nums = reduce(lambda x, y: x + y, nums, 10)
print(sum_nums)

# 字符串拼接
datas = ["ab", "cd", "e", "fg"]
new_data = reduce(lambda x, y: x + y, datas)
print(new_data)
