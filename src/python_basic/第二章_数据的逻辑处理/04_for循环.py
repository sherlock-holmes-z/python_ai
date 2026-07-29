import random

nums1 = "-".join(map(str, range(10)))  # range(end) 0-end,左闭右开
nums2 = "-".join(map(str, range(10, 20)))  # range(start,end),左闭右开
nums3 = "-".join(map(str, range(20, 30, 3)))  # range(start,end,step),左闭右开，步长为2
"""
map(str,range()) 将range中所有元素转成字符串类型，
'-'.join将所有元素以-连接
"""
print(nums1, nums2, nums3)


input_str = input("input str:")
for i in input_str:
    if i.isdigit():  # 判断字符是数字
        continue
    if i == "e":
        break
    print(f"元素{i}")
else:
    print("正常结束,break不会执行")
print("end")

"""嵌套循环"""
for i in range(10):
    for j in range(10):
        print(f"{i},{j}")
print("end")

random_num = random.randint(1, 100)
print(f"随机数字:{random_num}")
