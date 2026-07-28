"""
约定全大写变量表示常量，不希望被修改

python中没有真正意义上的常量机制，本质还是变量，只是约定好全大写不去修改，还是能修改成功
"""

MY_AGE = 18

NAME = 'zhangsan'

NAME = 'lisi'

print(NAME)
