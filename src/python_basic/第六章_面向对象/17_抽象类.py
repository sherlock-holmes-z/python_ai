"""
抽象类不能实例化，通过作为规范被子类继承，并实现其定义的抽象方法
"""

from abc import ABC, abstractmethod


# 继承ABC就表示是个抽象类
class MessageSender(ABC):
    # 定义抽象方法，不用实现
    @abstractmethod
    def send(self, content: str) -> None:
        """子类必须实现发送逻辑。"""

    def speak(self) -> None:
        print("hello ", self.__class__.__name__)


# 子类必须实现抽象方法，否则无法创建对象
class EmailSender(MessageSender): ...


class TextSender(MessageSender):
    def send(self, content: str) -> None:
        print(f"text: {content}")


if __name__ == "__main__":
    # 没有实现抽象方法，所以会报TypeError错
    # EmailSender()

    t = TextSender()
    t.send("message")  # 抽象方法
    t.speak()  # 继承抽象类的普通方法

"""
    什么时候用protocol？
    只需要约束所有方法，不用共享其他属性或统一方法，用protocol就行（java接口）
"""
