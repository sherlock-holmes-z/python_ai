# Python中操作文件的标准流程：
#   1.创建「文件对象」
#   2.操作文件（读取、写入 等）
#   3.关闭文件

# 文件操作的核心 —— open函数：它可以打开或创建文件，且支持多种操作模式，返回值是「文件对象」。
# open 函数最常用的三个参数如下：
#   1.file：要操作的文件路径
#   2.mode：文件的打开模式
#       r：读取（默认值）
#       w：写入，并先截断文件
#       x：排它性创建，如果文件已存在，则创建失败
#       a：打开文件用于写入，如果文件存在，则在文件末尾追加内容
#       b：二进制模式
#       t：文本模式（默认值）
#       +：打开用于更新（读取与写入）
#   3.encoding：字符编码

# 1.创建对象
# file = open(file='file/1.txt', mode='rt', encoding='utf-8')
# # 简写，rt是默认值
file = open('file/1.txt', encoding='utf-8')

# 操作文件：读取
result = file.read()
print(result)

# 关闭连接，不关闭就会一直占用运行内存
file.close()

# 读取二进制文件
file2 = open('file/2.class', mode='rb')
print(file2.read())
file2.close()

print('按字节读取')
# file3 = open('file/1.txt', encoding='utf-8')
# print(file3.read(4), end='')  # end= ''可以避免每次打印换行
# print(file3.read(5), end='')
# print(file3.read(6), end='')  # \n也算一个字符
# file3.close()

print('====循环按字节读取，对内存友好====')
file4 = open('file/1.txt', encoding='utf-8')
while True:
    line = file4.read(5)
    if not line:
        break
    print(line, end='')
file4.close()

print('=====循环按行读取====')
file5 = open('file/1.txt', encoding='utf-8')
while True:
    line = file5.readline(10)  # 按行读取，最多10个字符，少于10个也不会换行读
    if not line:
        break
    print(line.strip())
file5.close()

print('=====通过for直接迭代对象====')
file6 = open('file/1.txt', encoding='utf-8')
for line in file6:  # 一次迭代一行
    print(line.strip())
file6.close()

print('=====通过ReadLines一次读完所有放入列表====')
file7 = open('file/1.txt', encoding='utf-8')
lines = file7.readlines(15)  # 指定参数会读取指定的字符，字符超过一行才会读取下一行
print(lines)
file7.close()


print('=======with最佳实践，自动close========')
with open('file/1.txt', encoding='utf-8') as f:
    print(f.readlines())
