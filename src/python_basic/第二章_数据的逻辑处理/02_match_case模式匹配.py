day = input("输入星期几：")

match day:
    case "1":
        print("星期一")
    case "2":
        print("星期二")
    case "3" | "4":  # 匹配其中的任意一个
        print(f"day:{day}")
    case _:
        print("error")

my_list = ["get", "baidu.com", "google.com"]

match my_list:
    case ["get", url]:  # 匹配两个元素的list,且第一个元素为get
        print(url)
    case _ if len(my_list) == 3:  # 匹配后进行if判断
        print("error")
