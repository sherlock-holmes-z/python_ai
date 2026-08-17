num = int(input("input num:"))
while num > 0:
    print(num)
    num -= 1
    if num == 5:
        break
else:
    print("没有break，正常结束循环")
print("end")
