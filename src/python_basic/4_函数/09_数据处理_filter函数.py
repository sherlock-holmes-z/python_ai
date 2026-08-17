"""
从一组数据中筛选符合条件的元素，返回一组新数据
语法格式：filter(过滤函数，可迭代对象),过滤函数返回true保留
"""

nums = [1, 2, 3, 4, 5]
new_nums = filter(lambda num: num % 2 == 0, nums)
print(new_nums)  # 返回的也是迭代器对象
print(list(new_nums))

# 过滤非法字符串
names = ["zhangsan", "", None, "lisi"]
new_name = filter(lambda n: n, names)  # 空串和None为假值，会被转为false
print(list(new_name))

# 过滤成年人
person = [{"name": "zhangsan", "age": 18}, {"name": "lisi", "age": 16}, {"name": "wangwu", "age": 28}]
new_person = filter(lambda p: p["age"] >= 18, person)
print(list(new_person))
print(list(new_person))  # 迭代器对象已经被使用，再转list就为空[]

# 特殊用法,不传递过滤函数，会自动过滤假值
data = [0, 1, "", False, True, None, "a", [], {}, ()]
new_data = filter(None, data)
print(list(new_data))

"""
注意点：
延迟执行，不会立刻筛选，只有需要结果时才执行（遍历或转换）
返回的是迭代器对象，遍历或转换一次就会耗尽
会影响元素数量
"""
