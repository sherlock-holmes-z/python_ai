class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f"{self.name} speak")


# 定义Student类（子类，派生类），继承父类Person
class Student(Person):
    def __init__(self, name, age, stu_id):

        # 子类中，有两种方式调用父类的初始化方法，来实现对继承属性name,age的初始化
        # 方式一
        # super().__init__(name, age)

        # 方式二
        Person.__init__(self, name, age)

        #  子类独有的属性，自己手动初始化
        self.stu_id = stu_id


def speak():
    print("stu speak")


if __name__ == "__main__":
    stu = Student("zhangsan", 19, 1)
    print(stu.__dict__)

    stu.speak = speak  # 给实例stu添加speak方法后，下面会执行stu的speak方法

    # stu实例自身 -> Student类 -> Person类
    stu.speak()
