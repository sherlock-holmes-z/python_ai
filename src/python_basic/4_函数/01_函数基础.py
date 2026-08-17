"""
提前定义好、可以重复使用、实现特定功能的代码片段

函数可以不定义返回值类型，直接返回，不会报错，但会降低代码可读性
返回类型和定义的返回值类型不一致也能正常运行，但后续处理可能会报错
"""


def print_str(text: str) -> None:  # 没有 return 时，默认返回 None
    print(f"hello:{text}")


print_str("qwe")


# 单返回值
def calculate_total(price: float, quantity: int) -> float:
    return round(price * quantity, 2)  # 金额保留两位小数


total = calculate_total(9.99, 2)
print(total)


# 多个返回值会自动组包成元组返回
def get_user(user_id: int, name: str) -> tuple[int, str]:
    """
    这是函数的注释，返回id和转大写的name
    :param user_id: 用户 ID
    :param name: 姓名
    :return: id和姓名tuple
    """
    return user_id, name.upper()


user_id, user_name = get_user(1, "zhangsan")
print(user_id, user_name)


# 函数嵌套调用
def method_1() -> None:
    print(1)


def method_2() -> None:
    print("嵌套调用")
    method_1()
    print(2)


method_2()


def get_score(score_list: list[int]) -> tuple[int, int, float]:
    """
    返回成绩的最高分、最低分和平均分
    :param score_list:
    :return:
    """
    return max(score_list), min(score_list), round(sum(score_list) / len(score_list), 1)


print(get_score([1, 2, 3, 4, 5]))
