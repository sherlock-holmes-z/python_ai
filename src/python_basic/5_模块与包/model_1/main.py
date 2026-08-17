# 导入整个模块使用
import random

# 只导入模块中具体的功能点（函数，变量）
from math_utils import add, age, name

print(random.randint(1, 100))


result = add(1, 2)  # 导入了函数，可以直接调用函数使用
print(result)

print(name, age)  # 使用导入的变量
