"""
列表推导式
用简洁语句，从可迭代对象中，生成新列表的语法结构
语法格式：[表达式 for 变量 in 可迭代对象]
"""

## 需求：列表中每个元素变为原来的两倍
nums = [1, 2, 3, 4, 5]

# 方式一：map函数
result1 = list(map(lambda x: x * 2, nums))
print(result1)

# 方式二：fro循环+append
result2 = []
for num in nums:
    result2.append(num * 2)
print(result2)

# 方式三：列表推导式
result3 = [n * 2 for n in nums]
print(result3)

# 带条件的列表推导式
result4 = [n * 2 for n in nums if n % 2 == 0]
print(result4)

# 字典推导式
names = ['zhangsan', 'lisi', 'wangwu']
age = [17, 18, 19]
person = {names[i]: age[i] for i in range(len(names))}
print(person)

# 将多个序列一一配对，但不能处理数据
person_2 = dict(zip(names, age))
print(person_2)

# 集合推导式
new_names = {names[i] + str(age[i]) for i in range(len(names))}  # str不能直接+int
print(new_names)
