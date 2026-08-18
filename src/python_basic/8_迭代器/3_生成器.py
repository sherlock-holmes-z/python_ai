# 1.【生成器函数】:函数体中如果出现了yield关键字，那么这个函数就是【生成器函数】
# 2.【生成器对象】：调用【生成器函数】时，函数体不会立刻执行，而是返回一个【生成器对象】
# 备注：不管能否执行到yield所在位置，只要函数中有yield，那么这个函数就是【生成器函数】


def demo(num):
    if num > 10:
        yield 1
    yield 2


d = demo(1)
print(d)  # yield没有执行，仍然是generator object生成器对象


# 每次调用yield方法，都会从上一次暂停的位置继续运行到下一个yield
# yield后的表达式,或作为此次__next__方法的返回值
# 遇到return会StopIteration,并将return结果作为异常信息抛出
def demo2():
    print("第一")
    yield
    print("第二")
    yield 2
    print("第三")
    return "end"


d2 = demo2()
print(next(d2))  # yield后没有表达式，返回None
print(next(d2))
try:
    next(d2)
except StopIteration as e:
    print(f"抛出异常{e.value}")


def get_cars(num):
    for _ in range(num):
        yield f"第{_ + 1}辆车"  # yield可以写在for循环中


for c in get_cars(5):
    print(c)


# yield作用：产出一个值 + 暂停当前位置 + 下次从这里继续。（惰性遍历）
class Person2:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

        # self._attr = [name, age, height, weight]

    def get_fields(self):
        # yield self.name
        # yield self.age
        # yield self.height
        # yield self.weight

        # 简写
        # yield from self._attr
        yield from self.__dict__.values()


person2 = Person2("zhangsan", 19, 181.5, "80.0公斤")
# fro可以遍历生成器对象
for p in person2.get_fields():
    print(p)  # 遍历到哪条数据，哪条数据才会被加载进内存


# yield from把一个【可迭代对象】里的元素依次yield出去（替代for + yield）
# 适合组合加工，将分段产生的数据合并为一个新的生成器
# （比直接iter()的优势是惰性遍历，只有迭代到的分段数据才会加载进内存）
def get_nums():
    nums = [1, 2, 3, 4, 5]
    yield from nums
    # 等用于
    # for n in range(5):
    #     yield n


nums = get_nums()
print("nums:", next(nums))
print("nums:", next(nums))
print("nums:", next(nums))
print("nums:", next(nums))
print("nums:", next(nums))


class Person3:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def get_fields(self):
        yield from ("第一段", self.name, self.age)
        yield from ("第二段", self.height, self.weight)


person3 = Person3("33", 33, 33, 33.0)
for p in person3.get_fields():
    print(p)


# 使用生成器.send(值)，可以让生成器继续执行的同时，给上一次的yield传值
# next()只能取值，send()既能取值，也能传值
# 第一次启动生成器，不能传值！！！
def get_data():
    print("start")
    a = yield "第一次yield"
    print(a)
    b = yield "第二次yield"
    print(b)
    return "end"


data = get_data()
r1 = data.send(None)  # 第一次启动生成器不能传值，可以传None
print(r1)
r2 = data.send(111)  # 将111传给上一次yield的a
print(r2)
try:
    r3 = data.send(222)
    print("r3:", r3)
except StopIteration as e:
    print(e.value)


# 生成器实现fibo
def fibo(n):
    a, b = 1, 1
    for i in range(n):
        if i < 2:
            yield 1
        else:
            value = a + b
            a, b = b, value
            yield value


f = fibo(10)
for n in f:
    print(n)

# 无论是迭代器还是生成器，都可以使用list,tuple,set等直接拿到里面的所有内容（注意内存不要挤爆）
f2 = fibo(20)
print(list(f2))


# 生成器表达式：类似列表推导式的语法，快速创建生成器
# 语法格式：(表达式 for 变量 in 可迭代对象)
# 什么时候适合使用生成器表达式？？？  每个结果只依赖当前一个元素时使用
nums = [1, 2, 3, 4, 5]

# 列表推导式
new_nums_1 = [n * 2 for n in nums]
print(new_nums_1)

new_nums_2 = map(lambda n: n * 2, nums)
print(new_nums_2)
print(list(new_nums_2))

# 生成器表达式
generator_nums = (n * 2 for n in nums)
print(generator_nums)  # 返回的是一个生成器对象
for n in generator_nums:
    print(n)
