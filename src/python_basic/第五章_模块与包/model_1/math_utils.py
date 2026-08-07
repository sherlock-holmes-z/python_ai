"""
一个.py文件就是一个模块
"""

name = "zhangsan"

age = 21

height = 1.75

# 常量（使用大写，约定不修改（但并没有强制））
HAPPY = 'happy'
SAD = 'sad'

def greet():
    print("你好")


def add(left: int, right: int) -> int:
    return left + right


# 执行当前文件，执行main中代码；文件被导入，main中代码不执行
if __name__ == "__main__":
    print(add(20, 30))  # 测试代码放在main中

print(__name__)  # 当模块被导入时， __name__ 的值就是模块的名称
