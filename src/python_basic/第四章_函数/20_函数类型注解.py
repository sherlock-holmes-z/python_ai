# 示例4：设置 *args 的类型注解，要求 args 中的每个参数都必须是 int 类型
def add(*args: int) -> int:
    return sum(args)


# 示例5：设置 **kwargs 的类型注解，要求 kwargs 中的每组参数的值，必须是 str 或 int 类型
def show_info(**kwargs: str | int):
    print(kwargs)


# 获取函数的注解信息
print(show_info.__annotations__)  # {'kwargs': str | int}
