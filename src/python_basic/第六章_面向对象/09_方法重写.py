class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f"Person:{self.name},{self.age}")


class Student(Person):
    def __init__(self, id, name, age):
        super().__init__(name, age)
        self.id = id

    # 子类中定义一个与父类相同的方法，那么子类方法就会覆盖父类方法
    def speak(self):
        # super().speak()  # 调用父类方法
        print(f"Student:{self.id},{self.name},{self.age}")


if __name__ == "__main__":
    stu = Student(1, "zhangsan", 19)
    stu.speak()  # 调用子类方法

    # 判断对象是否为指定类或其子类的实例
    print(isinstance(stu, Person))

    # 判断类是否是其子类
    print(issubclass(Student, Person))
