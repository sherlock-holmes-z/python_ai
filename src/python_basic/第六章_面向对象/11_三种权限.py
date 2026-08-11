class Person:
    def __init__(self, name, age, height):
        self.name = name  # 公有属性，当前类，子类，类外部都可以访问
        self._age = age  # 受保护属性：当前类，子类中可以访问
        self.__height = height  # 私有属性：只能在当前类中访问

    def speak(self):
        print(f"name:{self.name},age:{self._age},height:{self.__height}")


class Student(Person):
    def __init__(self, name, age, height):
        Person.__init__(self, name, age, height)

    def speak(self):
        print(f"stu：name:{self.name},age:{self._age},height:{self.__height}")


if __name__ == "__main__":
    person = Person("lisi", 19, 19.9)
    person.speak()

    print(person._age)  # 受保护的属性，在类的外部，也能访问到，但是不推荐
    # print(person.__height) # 在类外部访问不了

    # py底层通过重命名方式实现私有属性，私有属性被转换成_Person__height
    print(person.__dict__)
    print(person._Person__height)  # 可以访问重命名属性，但不推荐

    # student = Student("lisi", 19, 19.9)
    # student.speak()  # 方法中访问不了父类的__height，会报错
