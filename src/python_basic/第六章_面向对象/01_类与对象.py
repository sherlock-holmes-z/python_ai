class Cat:
    pass  # 合法空操作，表示类/函数定义先空着，以后再补充


cat = Cat()
# 动态为对象添加属性
cat.name = "gulu"
cat.age = 5
print(cat.__dict__)  # 以字典的形式存储属性


class Dog:
    # 初始化方法，对象创建时自动调用，设置对象的初始状态
    # self表示当前创建的实例对象
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 定义在类外的叫函数，定义在类中函数叫方法，参数包含self
    def eat(self) -> str:
        return self.name + " eat boom"


dog = Dog(name="xiaohei", age=30)
print(dog.__dict__)
print(dog.eat())


class Bird:
    def __init__(self, name, skill="fly"):
        self.name = name
        self.skill = skill


bird = Bird(name="maque")  # 设置了默认值的属性，可以不初始化
print(bird.__dict__)
