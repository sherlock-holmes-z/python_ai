try:
    print("============")
    print(name)
    print("============")
except NameError as e:  # 捕获NameError异常
    print("name error: ", e)
finally:
    print("finally")  # 一定会执行
