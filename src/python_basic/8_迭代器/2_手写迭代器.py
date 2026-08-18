# 迭代器是一次性的，状态只会向前推进，且不会自动重置（迭代器在遍历的过程中会被消耗）

# for循环可以遍历person的实例对象
class Person:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def __iter__(self):
        return iter([self.name, self.age, self.height, self.weight])  # 直接返回全量数据的迭代器


person = Person("zhangsan", 19, 181, 80.0)
for p in iter(person):
    print(p)


class Fibo:
    def __init__(self, total):
        self.total = total
        self.i = 0
        self.a = 1
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.total:
            raise StopIteration
        elif self.i < 2:
            result = 1
        else:
            result = self.a + self.b
            self.a = self.b
            self.b = result
        self.i += 1
        return result  # py中只要变量在执行过程中创建，就可以在后续被使用（上面的if else中必定会定义result）


f = Fibo(10)  # 不使用时，迭代器中的数据不会生成，不占用内存，惰性按需计算
for n in f:
    print(n)


# 不使用迭代器，直接将所有数据计算加载进内存
def fibo_2(total):
    if total == 1:
        result = [1]
    elif total == 2:
        result = [1, 1]
    elif total > 2:
        result = [1, 1]
        for i in range(2, total):
            result.append(result[-1] + result[-2])
    return result


for n in fibo_2(10):
    print(n)
