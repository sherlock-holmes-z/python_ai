"""
在 Python 中，推荐用 Protocol 描述接口约束；如果多个实现还需要共享通用逻辑和状态，再使用抽象基类
"""

from typing import Protocol


# notify方法定义了对象是MessageSender类型 使用Protocol会让编辑器检查传入的对象有没有包含MessageSender的方法
# 如果传入的对象包含了，就不会警告，如果没有全包含就会提前警告（类似于java接口）
class MessageSender(Protocol):
    def send(self, content: str) -> None: ...  # ...和pass类似，表示接口声明，不作实现


class SmsSender:
    def send(self, content: str) -> None:
        print(f"发送短信：{content}")


class EmailSender:
    def send(self, content: str) -> None:
        print(f"发送邮件：{content}")


def notify(sender: MessageSender, content: str) -> None:
    sender.send(content)


if __name__ == "__main__":
    notify(SmsSender(), "订单已支付")
    notify(EmailSender(), "订单已支付")
