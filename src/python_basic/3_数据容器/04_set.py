"""无序、元素唯一、元素可hash、可变、没有索引，不能用 set[0] 访问。"""

print("========创建集合=========")
empty_set = set()  # 创建空集合,只能这样创建
no_empty_set = {}  # 这种创建方式得到的是dict
print(type(no_empty_set))  # dict

set2 = set([1, 2, 2, 3, 3])  # 从包含重复元素的列表创建集合
print(set2)
list1 = [1, 2, 3, 3, "a", "b", "c"]
set3 = set(list1)
print(set3)

print("========集合操作=========")
tags_set = {"java", "vue"}
print("java" in tags_set)

tags_set.add("python")
print(tags_set)

tags_set.update({"python", "c++"})  # 批量添加元素
print(tags_set)

tags_set.remove("python")  # 删除元素，元素不存在会报错
print(tags_set)

tags_set.discard("unknow")  # 删除元素，不存在不会报错
print(tags_set)

print(tags_set.pop())  # 删除并返回任意一个元素
print(tags_set)

tags_set.clear()  # 清空元素
print(tags_set)

print("========集合运算=========")
python_skills = {"python", "sql", "docker"}
ai_skills = {"python", "llm", "rag"}

print(python_skills | ai_skills)  # 并集：全部技能
print(python_skills.union(ai_skills))

print(python_skills & ai_skills)  # 交集：共同技能
print(python_skills.intersection(ai_skills))

print(python_skills - ai_skills)  # 差集：仅前者有
print(python_skills.difference(ai_skills))

print(python_skills ^ ai_skills)  # 对称差：双方不同的部分
print(python_skills.symmetric_difference(ai_skills))

print("========子集与超集的判断=========")  # （适合权限和配置校验）
required = {"python", "sql"}
candidate = {"python", "sql", "docker"}
required.issubset(candidate)  # True required是candidate的子集
candidate.issuperset(required)  # True candidate是required的超集

print("========去重保持原顺序=========")
tags = ["python", "ai", "python", "rag", "abc"]
unique_tags = list(set(tags))  # list使用set去重，list的顺序会变
print(unique_tags)
list_tags = list(dict.fromkeys(tags, 0))  # 使用list转dict的key去重，顺序不变
print(list_tags)

print("========元素的可hash限制=========")
valid_set = {1, "python", (1, 2)}  # 元组通常可以放入 set，但内部不能包含不可哈希对象

# list
# {[1, 2]}                 # TypeError: unhashable type: 'list'
#
# # dict
# {{"name": "Python"}}     # TypeError: unhashable type: 'dict'
#
# # set
# {{1, 2}}                 # TypeError: unhashable type: 'set'
#
# # bytearray
# {bytearray(b"abc")}      # TypeError: unhashable type: 'bytearray'

hash("python")  # 正常
# hash([1, 2])    # TypeError 通过能否hash判断能不能放入set

# sort的作用是将dict内容相同，顺序不同的字典转化为相同的结果
# {"timeout": 10, "retry": 3}和{"retry": 3, "timeout": 10}转化后相同
configurations = tuple(sorted({"timeout": 10, "retry": 3}.items()))
print(configurations)

frozen_set = frozenset({1, 2})
frozen_set = frozen_set.union(frozenset({3, 4}))
print(frozen_set)
# frozenset不可变set可以hash
abnormal_set = {frozenset({1, 2}), (1, 2), configurations}
print(abnormal_set)
