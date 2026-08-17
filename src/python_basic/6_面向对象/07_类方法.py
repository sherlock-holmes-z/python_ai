from datetime import datetime


class Person:
    version = "v1.0.0"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 类方法通常实现与类有关的逻辑
    # 接收类本身cls，和自定义参数，通过cls访问类属性
    # 类方法通常实现与类相关的逻辑，例如：操作类信息，工厂方法
    @classmethod
    def change_version(cls, new_version):
        cls.version = new_version

    @classmethod
    def create_person(cls, name, birth_year):
        age = datetime.now().year - birth_year
        return Person(name, age)


if __name__ == "__main__":
    Person.change_version("v1.0.1")
    print(Person.version)

    person = Person.create_person("zhangsan", 1996)
    print(person.__dict__)

    # 类方法也能通过实例调用，但是不推荐
