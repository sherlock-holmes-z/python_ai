"""
1.能被for循环遍历的对象，被称为可迭代对象:iterable
2.可迭代对象能调用__iter__方法
3.调用__iter__()会得到一个迭代器，等价于iter(对象)

"""

names = ["zhangsan", "lisi"]
for name in names:
    print(name)

print(hasattr(names, "__iter__"))  # 判断对象中有没有某个属性
names_iter = names.__iter__()
print(names_iter)


strs = "vue"
for s in strs:
    print(s)
str_iter = iter(strs)

# 迭代器遍历
while True:
    try:
        print(next(str_iter))  # 迭代器的next方法，每次调用都会根据当前状态，返回下一个元素
    except StopIteration:  # 后续没有元素可调用next抛出停止迭代异常
        break
