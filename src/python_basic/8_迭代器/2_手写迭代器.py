# 迭代器是一次性的，状态只会向前推进，且不会自动重置（迭代器在遍历的过程中会被消耗）

# for循环可以遍历person的实例对象
class Person:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def __iter__(self):
        return iter([self.name, self.age, self.height, self.weight])


person = Person("zhangsan", 19, 181, 80.0)
for p in iter(person):
    print(p)


# yield作用：产出一个值 + 暂停当前位置 + 下次从这里继续。
class Person2:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def get_fields(self):
        yield self.name
        yield self.age
        yield self.height
        yield self.weight


person2 = Person2("zhangsan", 19, 181, 80.0)
for p in person2.get_fields():
    print(p)


# yield from适合组合加工，分段产生数据
class Person3:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def get_fields(self):
        yield from iter(("第一段", self.name, self.age))
        yield from iter(("第二段", self.height, self.weight))


person3 = Person3("33", 33, 33, 33.0)
for p in person3.get_fields():
    print(p)
