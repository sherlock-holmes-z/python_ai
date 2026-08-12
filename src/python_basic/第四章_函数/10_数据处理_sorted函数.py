"""
对一组数据进行排序，返回新数据
语法格式：sorted(可迭代对象，key=xxx,reverse=Ture/False)
"""

# 数字排序
nums = [3, 6, 1, 7]
new_nums = sorted(nums, reverse=True)  # 默认False,从小到大排序；Ture从大到小
print(new_nums)

names = ["python", "java", "js", "vue"]
# new_names = sorted(names, key=lambda x: len(x))
new_names = sorted(names, key=len)  # 简写
print(new_names)

person = [{"name": "zhangsan", "age": 18}, {"name": "lisi", "age": 16}, {"name": "wangwu", "age": 28}]
new_person = sorted(person, key=lambda p: p["age"], reverse=True)
print(new_person)

# max,min也可传递key参数，用于设置筛选依据
max_person = max(new_person, key=lambda p: p["age"])  # 年龄最大
print(max_person)

min_person = min(new_person, key=lambda p: p["age"])  # 年龄最小
print(min_person)
