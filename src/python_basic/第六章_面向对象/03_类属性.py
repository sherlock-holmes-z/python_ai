class Car:
    # 类属性，所有实例共享，类名.属性
    wheels = 4
    tax_rate = 0.1

    def __init__(self, name, price):
        self.name = name
        self.price = price


print(Car.wheels, Car.tax_rate)
car1 = Car("car1", 100)
print(car1.wheels)
car1.wheels = 5  # 并不会修改类属性，而是给实例对象增加了一个实例属性
print(car1.wheels)
print(Car.wheels)  # 类属性不变

print(car1.wheels)  # 实例对象.属性，会先找实例属性，没有再找类属性

Car.wheels = 10  # 真正修改类属性
print(Car.wheels)
