# 指定from ... import * 导入的是哪些功能
__all__ = ["NAME"]

NAME = "张三"

AGE = 18


def print_str(content: str):
    print("print_str:", content.upper())
