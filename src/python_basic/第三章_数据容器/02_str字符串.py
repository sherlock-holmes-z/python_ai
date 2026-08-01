"""有序，不可变，字符序列，通过索引访问。用途：文本处理"""

# 不可变对象，使用方法后原字符串不会改变，方法要用新字符串变量接收
str_1 = ' hello python GULU '
print(str_1[0]) # 字符串有下标
print(str_1[0:5:2]) # 字符串可切片

print(str_1.find('python')) # 返回下标，找不到返回-1
print(str_1.index('python'))  # 找不到报错

print(str_1.count('python'))

print(str_1.upper())
print(str_1.lower())

print(str_1.replace('python', 'Java'))

print(str_1.strip())
print(str_1.lstrip())
print(str_1.rstrip())
