class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        return self.name, self.age


class Worker:
    def __init__(self, job):
        self.job = job

    def get_job(self):
        return self.job


# 多继承
class Child(Person, Worker):
    def __init__(self, name, age, job):
        Person.__init__(self, name, age)
        Worker.__init__(self, job)


if __name__ == "__main__":
    child = Child("lisi", 19, "it")
    info = child.get_info()
    job = child.get_job()
    all_info = (*info, job)  # 元组先解包，在与新元素组包
    print("--".join(map(str, all_info)))  # map是将元祖中所有元素转为字符串

    # 用来记录子类属性和方法的查找顺序
    print(Child.__mro__)
