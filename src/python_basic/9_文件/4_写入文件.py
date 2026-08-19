# 文件操作的核心 —— open函数：它可以打开或创建文件，且支持多种操作模式，返回值是「文件对象」。
# open 函数最常用的三个参数如下：
#   1.file：要操作的文件路径
#   2.mode：文件的打开模式
#       r：读取（默认值）
#       w：写入，并先截断文件（即先清空文件内容）
#       x：排它性创建，如果文件已存在，则创建失败
#       a：打开文件用于写入，如果文件存在，则在文件末尾追加内容
#       b：二进制模式
#       t：文本模式（默认值）
#       +：打开用于更新（读取与写入）
#   3.encoding：字符编码
import time

# w模式，写之前会清空文件内容
with open('file/a.txt', mode='wt', encoding='utf-8') as f:
    f.write('hello world2')

# x模式，文件存在，创建失败
# with open('file/b.txt', mode='xt', encoding='utf-8') as f:
#     f.write('hello world3')

# a模式，追加写入
with open('file/c.txt', mode='at', encoding='utf-8') as f:
    f.write('hello ')

# py写入时，不是没写一次立刻落盘，而是写到缓冲区，结束后落盘
with open('file/d.txt', mode='at', encoding='utf-8') as f:
    f.write('1')
    f.write('2')
    # f.flush() # 手动刷盘
    time.sleep(10)  # 单位是秒，执行到这里时文件中没有写入ab
    f.write('3')
    f.write('4')
