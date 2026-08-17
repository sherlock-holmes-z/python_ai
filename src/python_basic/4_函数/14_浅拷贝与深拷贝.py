import copy

# 浅拷贝：创建一个新的外层容器，但内部元素仍然引用原来的对象
nums = [1, 2, 3, 4, [5, 5]]
new_nums = copy.copy(nums)
print(new_nums)
new_nums[4][0] = 6  # 新容器修改内部可变对象，原容器也会被修改
print('nums', nums)
print('new_nums', new_nums)

# 深拷贝：创建一个新的外层容器,并对内部所有的可变对象进行复制
nums_2 = [1, 2, 3, 4, [5, 5]]
new_nums_2 = copy.deepcopy(nums_2)
print(nums_2)
new_nums_2[4][0] = 6  # 新容器修改可变对象不影响原容器
print('nums_2', nums_2)
print('new_nums_2', new_nums_2)
