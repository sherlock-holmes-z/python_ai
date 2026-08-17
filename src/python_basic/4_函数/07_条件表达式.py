def normal_function(age):
    if age >= 18:
        return "成年"
    else:
        return "未成年"


def function2(age):
    # 条件表达式，适合简单的二选一场景
    return "成年" if age >= 18 else "未成年"


if __name__ == "__main__":
    print(function2(17))
