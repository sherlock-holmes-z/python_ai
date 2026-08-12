"""
map函数：对一组数据中的每一个函数，统一执行某个操作，生成新的一组数据
语法格式：map(函数操作，可迭代对象)
"""

nums = [1, 2, 3, 4]

# map的返回值是一个迭代器对象，需要手动遍历或类型转换
nums = map(lambda x: x * 2, nums)
print(list(nums))

names = ["java,python "]
new_names = map(lambda x: x.upper(), names)
print(list(new_names))


"""
注意：
map是延迟执行，不会立刻计算，只有在需要结果的时候才会计算
map返回值是一个迭代器对象，遍历完成或者转换之后就会被耗尽
map不会影响元素的数量
"""
