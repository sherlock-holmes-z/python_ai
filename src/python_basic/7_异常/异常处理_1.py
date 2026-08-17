try:
    a = input("请输入第一个数")
    b = input("请输入第二个数")
    print("计算结果：", a / b)
except (ZeroDivisionError, ValueError) as e:
    print("捕获异常", e)
except Exception as e:
    print("兜底异常", e)
else:
    print("正常结束")
finally:
    print("一定会执行")
