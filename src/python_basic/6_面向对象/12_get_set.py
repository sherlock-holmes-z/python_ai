class Person:
    def __init__(self, name, age, idcard):
        self.name = name
        self._age = age
        self._idcard = idcard

    # 注册_age属性的get方法，当访问实例的age属性时，就会调用age方法
    @property
    def age(self):
        return self._age

    # 注册age属性的set方法，当修改age属性时，下面的方法就会调用
    # 主要作用：赋值时统一校验，避免非法数据进入对象
    @age.setter
    def age(self, age):
        if 0 < age < 120:
            self._age = age
        else:
            print("年龄异常")
            # raise ValueError("年龄错误")

    # 获取身份证号返回结果加密
    @property
    def idcard(self):
        return self._idcard[:6] + "*" * 8 + self._idcard[-4:]

    @idcard.setter
    def idcard(self, idcard):
        print("idcard cannt change")


if __name__ == "__main__":
    person = Person("lisi", 18, "340421199601204010")
    # print(person.age())
    print(person.name)
    print(person.age)
    person.age = 120
    print(person.age)

    print(person.idcard)  # 获取加密身份证号
    person.idcard = "new card"  # 修改失败
