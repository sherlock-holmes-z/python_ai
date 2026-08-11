class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == "__main__":
    # 所有类都继承object类
    print(issubclass(int, object))
    print(isinstance(tuple, object))
    print(isinstance(str, object))
    print(isinstance(set, object))
    print(isinstance(dict, object))

    person = Person("lisi", 18)
    print(person.__dict__)  # 对象自己的属性
    print(object.__dict__.keys())
    print(dir(person))  # 对象可以访问到的属性，除自己的属性外，其他都是继承object的

    # 两个输出一样，因为都是obj提供的能力
    print(person)
    print(person.__str__())
