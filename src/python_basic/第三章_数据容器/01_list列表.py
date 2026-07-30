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

"""常用方法"""
num_list = [3, 1, 2]
print(num_list)

num_list.append(4)  # 末尾追加
print(num_list)

num_list.insert(0, 0)  # 在指定索引处插入
print(num_list)

num_list.extend([5, 6])  # 合并另一个可迭代对象
print(f"extend:{num_list}")
num_list = num_list + [7, 8, 9]
print(f"使用+号合并:{num_list}")

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

num_list.clear()  # 清空列表
print(num_list)

print("========切片=========")
cut_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 起始为0,，步长为1，这三个写法效果相同
print(cut_nums[0:5:1])
print(cut_nums[0:5])
print(cut_nums[:5])


print("========浅拷贝=========")
original_list = list(range(1, 5))
copy_list = original_list.copy()  # 此时，两个列表的每个元素都指向同一个对象
copy_list[1] = 9  # 关键操作：将 copy_list 的索引 1 重新指向了一个新的字符串对象 '9'
print(f"original_list{original_list}")  # original_list没有改变，因为引用对象没变

list_1 = [[1, 1], [2, 2]]
list_copy = list_1.copy()
print(f"before update:{list_1},{list_copy}")
list_copy[0].append(1)
print(f"after update:{list_1},{list_copy}")

print("========= 解包 ==================")
jb_list = ["zhangsan", 18, "man", "180cm"]
name, age, gender, height = jb_list
print(f"name:{name},age:{age},gender:{gender},height:{height}")

# *可以接受剩余元素
a, *b, c = jb_list
print(f"a:{a},b:{b},c:{c}")

# 企业代码里常用于解析固定结构的数据，例如数据库查询结果、函数多返回值、配置项
status_code, data = 200, {"id": 1, "name": "zhangsan"}

# 使用解包组包合并列表
nums_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9]
nums_2 = [7, 8, 9, 10]
nums_3 = [*nums_1, *nums_2]
print(f"解包组包方式：{nums_3}")


print("=========推导式=====")
nums = [1, 2, 3, 4]
nums_2 = [n**2 for n in nums]  # nums中所有元素的2次方
print(nums_2)
nums_3 = [n**2 for n in nums if n % 2 == 0]  # 筛选nums中%2=0的数，二次方
print(nums_3)
nums_4 = [n**2 for n in range(1, 21)]
print(nums_4)

raw_texts = ["  Python ", "", " AI  ", "  "]
# text.strip()移除首位的空字符串，返回非空if为true
cleaned_texts = [text.strip().lower() for text in raw_texts if text.strip()]
print(cleaned_texts)  # ['python', 'ai']

print("========练习合并列表并去除重复元素")
nums_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9]
nums_2 = [7, 8, 9, 10]
for num in nums_2:
    if num not in nums_1:
        nums_1.append(num)
print("普通遍历判断append方式：", nums_1)

nums_set = []
nums_set.extend(nums_1)
nums_set.extend(nums_2)
print("转set去重方式：", set(nums_set))
