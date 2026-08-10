class Car:
    # 也是一个魔法方法
    def __init__(self, name: str, count: int, price: float | int):
        self.name = name
        self.count = count
        self.price = price

    # 定义实例方法,参数self
    def total_price(self):
        return self.price * self.count

    # 定义类方法，不需要创建对象，类名直接调用,参数clas
    @classmethod
    def car_info(cls):
        print("this is car class method")

    # 魔法方法
    # 重写toString方法
    def __str__(self):
        return f"{self.name} {self.count} {self.price}"

    # 重写eq
    def __eq__(self, other: object):
        if not isinstance(other, Car):
            return False
        return self.name == other.name and self.count == other.count

    # 重写lt
    def __lt__(self, other):
        return self.count * self.price < other.count * other.price


car = Car("bmw", 2, 19.99)
print(car)  # 默认输出对象的地址，通过魔法方法__str__可以重写输出内容
car2 = Car("bmw", 10, 39.99)
print(f"eq:{car == car2}")  # 执行__eq__比较
print(f"lt:{car < car2}")  # 执行__lt__比较
print(car.total_price())

Car.car_info()
