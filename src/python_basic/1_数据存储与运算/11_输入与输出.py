name = input("please input your name:")
weight = float(input("please input your weight:"))

print(f"your name is {name} and your weight is {weight}")


total_money = 1000

pwd = input("please input your password:")
if pwd == "123456":
    take_money = int(input("please input your take money:"))
    total_money -= take_money
    print(f"your total money is {total_money}")
else:
    print("password error")
