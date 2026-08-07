# 绝对路径导入：从当前文件所在目录查找
from package_1 import tools, tools_2

# 绝对路径导入：从项目根目录往下查找
from python_basic.第五章_模块与包.package_1 import tools, tools_2

# 不使用import * 就可以导入tools_2
tools.print_hello()
tools_2.print_hello()
