"""

有序，不可变，允许重复，通过索引访问。类似只读列表。用途：字典键，固定数据。

"""

print("=========创建元组===========")
user = ("张三", 18, "北京")
empty_tuple = ()
single_tuple = (1,)  # 单元素元祖必须加逗号
single_int = 1

user_2 = "张三", 18, "shanghai"  # 括号可以省略，真正决定元组的是逗号
print(type(user_2))

# 元组是有序序列，访问方式与列表相同：
skills = ("Python", "Java", "SQL", "Docker")
print(skills[0])  # Python
print(skills[-1])  # Docker
print(skills[1:3])  # ('Java', 'SQL')
print(skills[::-1])  # 步长-1，反转后的新元组

# 不可变，创建后不能修改
skills = ("Python", "Java")
# skills[0] = "Go" # TypeError

# 元组不可变，指的是元组保存的引用不能改变。如果里面放了列表，列表自身仍然可以修改：
data = ("张三", ["Python", "Java"])
data[1].append("SQL")
# file[1] = [2] # 但不能让data[1]指向另一个列表
print(data)

print("=========遍历与成员判断===========")
skills_2 = ("Python", "Java", "SQL")
for skill in skills_2:
    print(skill)
print("Python" in skills_2)  # True
print("Go" not in skills_2)  # True
print(len(skills_2))  # 3

for index, skill in enumerate(skills):
    print("需要索引时：", index, skill)

print("=========元组只有两个常用方法：count，index===========")
numbers = (1, 2, 2, 3)
print(numbers.count(2))  # 2，统计出现次数
print(numbers.index(3))  # 3，查找首次出现位置。index找不到会报错


print("=========解包===========")
# 组包：多个独立值合并为一个元组
# 解包：一个元组分解为多个变量
user = "张三", 18, "北京"
name, age, city = user
print(name, age, city)
name, *other = user
print(name, other)

print("=========元组与列表互换===========")
skills_tuple = ("Python", "Java")
skills_list = list(skills_tuple)
skills_list.append("SQL")
new_tuple = tuple(skills_list)
print(new_tuple)
# 需要频繁增删时使用列表；数据确定后可以转成元组
