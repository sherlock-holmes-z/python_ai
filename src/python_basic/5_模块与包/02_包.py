# 绝对路径导入：从当前文件所在目录查找
import numpy as np
from package_1 import tools, tools_2

# 绝对路径导入：从项目根目录往下查找
# from python_basic.5_模块与包.package_1 import tools, tools_2

# 不使用import * 就可以导入tools_2
tools.print_hello()
tools_2.print_hello()

scores = np.array([90, 85, 100])

new_scores = scores + 5
print(new_scores)  # [ 95  90 105]
