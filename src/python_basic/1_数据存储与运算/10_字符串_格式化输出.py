name = 'zhangsan'
age = 22
weight = 79.9
is_man = True

# 写法一：拼接，字符串只能拼接字符串，所以整型要转字符串
info_1 = '字符串拼接：我叫' + name + '年龄' + str(age)
print(info_1)

# 写法二：占位符
# 整型，浮点，布尔型都可以使用%s占位，会自动转为字符串，布尔值没有自己的占位符，就是%s
info_2 = '我是%s,年龄%s,体重%s,是男%s' % (name, age, weight, is_man)
print(info_2)

# %i整型占位符，%f浮点型占位符（会有精度问题）
info_3 = '使用对应格式占位符,我是%s,年龄%i,体重%f,是男%s' % (name, age, weight, is_man)
print(info_3)

# f-string占位方式
info_4 = f'f-string占位：我是{name}'
print(info_4)

info_5 = 'format占位：体重{}'.format(weight)
print(info_5)
