# round是四舍五入
# 但是银行家舍入法：小于5舍，大于5入，等于5看奇偶（奇入偶舍）
print(round(3.5))  # 4
print(round(4.6))  # 5
print(round(5.4))  # 5
print(round(6.5))  # 6
print(round(7.6))  # 8

print(round(7.666, 2))  # 保留两位小数

# 将多个序列一一配对，但不能处理数据，数量不一致谁少跟谁走
names = ['zhangsan', 'lisi']
age = [17, 18, 19]
person_2 = dict(zip(names, age))
print(person_2)

# 逻辑判断
print(all(['1', 0]))  # 全为真返回true ,0是假值
print(any(['1', 0]))  # 有一个为真返回true
