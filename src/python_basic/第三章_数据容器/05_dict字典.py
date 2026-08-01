"""
无序（在 3.7+ 中是有序插入），可变，通过键（任意不可变类型）访问，键必须唯一，值可以是任意类型
用途：键值映射。
"""
import copy

print("==========创建字典==========")
# key 必须可哈希，例如 int、str；如果是 tuple，其内部元素也必须可哈希
user = dict([("name", "张三"), ("age", 18), ("city", "北京"), ((10, 20), "坐标"), ("name", "lisi")])
print(user)  # key 重复时，后面的值会覆盖前面的值
empty_dict = {}
another_empty = dict()

print(user["name"])  # 键不存在会报错
print(user.get("no_name"))  # 键不存在不会报错。返回None

print("==========增删改==========")
user_2 = {"name": "wangwu", "city": "shanghai", "sex": "nan"}
user_2["name"] = "upd_wangwu"
user_2["age"] = 18
user_2["last_key"] = "last_value"
print(user_2)
print(user_2)

if "age" in user_2:
    del user_2["age"]  # 删除key-value，没有会报错
print(user_2)

if "name" in user_2:
    name = user_2.pop("name")  # 删除并返回value，没有会报错
    print(user_2, name)

no_key = user_2.pop("no_key", None)  # 安全删除，没有返回默认值None
print(user_2, no_key)

if len(user_2) > 0:
    k, v = user_2.popitem()  # 删除并返回最后插入的k-v,如果是个空字典也会报错
    print(user_2, k, v)

user_2.clear()  # 清空
print(user_2)


print("==========判断键，值是否存在==========")
user = {"name": "张三", "age": 18}
print("name" in user)  # True
print("email" not in user)  # True
print("张三" in user.values())  # True 判断值
print("zhangsan" in user.values())

print("==========遍历key,value==========")
for key in user:  # 只遍历key
    print(key)

for value in user.values():  # 只遍历value
    print(value)

for key, value in user.items():  # 同时遍历k-v,这里使用了解包自动给kv赋值
    print(key, value)

print(type(user.keys()))  # 键视图
print(type(user.values()))  # 值视图
print(type(user.items()))  # 键值对视图

# 视图是动态的，如果原字典发生改变，视图也会发生变化
keys = user.keys()
user["city"] = "北京"
print(keys)  # 包含 city


print("==========合并与批量更新==========")
config = {"timeout": 10, "retry": 2}
config.update(
    {
        "timeout": 30,
        "debug": True,
    }
)
print(config)

default_config = {"timeout": 10, "retry": 2}
# 字典的解包用双星号**，单信号是列表和元组的解包方式
prod_config = {**default_config, "timeout": 30}  # 先解包后，与后面的元素合成一个新字典，key相同时，右侧覆盖左侧
print(prod_config)

# 或者
prod_config = default_config | {"timeout": "new30"}  # key相同时，右侧覆盖左侧
print(prod_config)

print("==========字典推导式==========")
numbers = [1, 2, 3, 4]
new_numbers_set = {num: num**2 for num in numbers}
print(new_numbers_set)

print("==========嵌套字典==========")
response = {
    "code": 200,
    "data": {
        "user": {
            "id": 1,
            "name": "张三",
        }
    },
}
print(response["data"]["user"]["name"])  # 如果其中一个key不存在，就会报错
# 层级和结构不确定时，需要逐层校验
data = response.get("data", {})
user = data.get("user", {})
name = user.get("name2")
print(name)

print("==========字典拷贝==========")
original = {"name": "张三"}
copy_data = original
copy_data["name"] = "李四"
print(original)  # 也被修改，直接赋值两个变量共用一个字典对象，指向同一个内存

# 浅拷贝：创建一个新字典对象，但新对象元素不新建，指向原对象
original = {"tags": ["python", "ai"], "name": "original"}
copy_data = original.copy()
copy_data["tags"].append("rag")  # 修改新字典的可变对象，就是修改原字典的可变对象
copy_data["name"] = "copy_data"  # 修改新字典的不可变对象，等于换了一个新的引用，不在指向原对象
print(original)

# 深拷贝，创建新对象，内部元素也全部新建
original = {"tags": ["python", "ai"]}
copy_data = copy.deepcopy(original)
copy_data["tags"].append("rag")
print(original)  # {'tags': ['python', 'ai']} ← 没变！
print(copy_data) # {'tags': ['python', 'ai', 'rag']}


print("==========字典顺序==========")
data = {"a": 1, "c": 2, "b": 3}
print(data) # 字典的顺序是插入顺序，也可排序
sorted_items = sorted(data.items())
print(sorted_items)

print("==========字典类型==========")
scores: dict[str, int] = {
    "语文": 90,
    "数学": 95,
}

user: dict[str, str | int] = {
    "name": "张三",
    "age": 18,
}
