"""
如果它像鸭子一样能走、能叫，就可以当作鸭子使用。
也就是说，不一定非要继承同一个父类；只要接口行为一致即可。
"""


class Dog:
    def speak(self) -> str:
        return "汪汪"


class Cat:
    def speak(self) -> str:
        return "喵喵"


def make_sound(animal) -> None:
    print(animal.speak())


if __name__ == "__main__":
    make_sound(Dog())
    make_sound(Cat())
