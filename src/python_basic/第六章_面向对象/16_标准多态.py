"""
标准多态，子类继承父类重写方法
"""


class MessageSender:
    def send(self, content: str) -> None: ...


class SmsSender(MessageSender):
    def send(self, content: str) -> None:
        print(f"发送短信：{content}")


class EmailSender(MessageSender):
    def send(self, content: str) -> None:
        print(f"发送邮件：{content}")


def notify(sender: MessageSender, content) -> None:
    sender.send(content)


if __name__ == "__main__":
    notify(SmsSender(), "订单已支付")
    notify(EmailSender(), "订单已支付")
