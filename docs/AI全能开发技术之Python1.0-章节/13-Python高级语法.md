# Python高级语法

## 浅拷贝与深拷贝

- 直接赋值：对象的引用（别名），不产生拷贝。

- 浅拷贝：拷贝父对象，不会拷贝对象的内部的子对象。拷贝后只有第一层是独立的。

- 深拷贝：完全拷贝了父对象及其子对象。拷贝后所有层都是独立的。

### 如何浅拷贝

- 切片操作（如 [:]）。

- 使用工厂函数（如 list() / set()）。

- 使用 copy 模块的 copy() 函数。

### 案例

##### 创建一个列表，其中包含整型和列表元素，使用 copy() 对其浅拷贝。使用 id() 查看列表地址和列表中各个元素的地址。

```python
import copy

list1 = [1, 2, 3, [100, 200, 300]]
print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
# 3060924684544 140732039489976 140732039490008 140732039490040 3060924682624 [1, 2, 3, [100, 200, 300]]

list2 = copy.copy(list1)
print(id(list2), id(list2[0]), id(list2[1]), id(list2[2]), id(list2[3]), list2)
# 3060926299456 140732039489976 140732039490008 140732039490040 3060924682624 [1, 2, 3, [100, 200, 300]]
```

可以看到拷贝后新的列表地址改变了，但列表中各个元素还是同一地址。

![image93](../assets/python1.0/image93.png)

##### 修改 list1[0] 整型元素

```python
list1[0] = 100  # 修改list1[0]整型元素

print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
# 3060924684544 140732039493144 140732039490008 140732039490040 3060924682624 [100, 2, 3, [100, 200, 300]]

print(id(list2), id(list2[0]), id(list2[1]), id(list2[2]), id(list2[3]), list2)
# 3060926299456 140732039489976 140732039490008 140732039490040 3060924682624 [1, 2, 3, [100, 200, 300]]
```

list[0] 为不可变类型元素，因此可以看到 list[0] 指向了新的引用。

![image94](../assets/python1.0/image94.png)

##### 修改 list[3] 列表元素

```python
list1[3].append(400)  # 修改list1[3]列表元素，向列表中添加新值

print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
# 3060924684544 140732039493144 140732039490008 140732039490040 3060924682624 [100, 2, 3, [100, 200, 300, 400]]

print(id(list2), id(list2[0]), id(list2[1]), id(list2[2]), id(list2[3]), list2)
# 3060926299456 140732039489976 140732039490008 140732039490040 3060924682624 [1, 2, 3, [100, 200, 300, 400]]
```

list[3] 为可变类型元素，修改不会产生新对象。

![image95](../assets/python1.0/image95.png)

### 如何深拷贝

使用 copy 模块的 deepcopy() 函数。

### 案例

##### 创建一个列表，其中包含整型和列表元素，使用 deepcopy() 对其深拷贝。使用 id() 查看列表地址和列表中各个元素的地址。

```python
import copy

list1 = [1, 2, 3, [100, 200, 300]]
print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
# 3060924684544 140732039489976 140732039490008 140732039490040 3060924682624 [1, 2, 3, [100, 200, 300]]

list3 = copy.deepcopy(list1)
print(id(list3), id(list3[0]), id(list3[1]), id(list3[2]), id(list3[3]), list3)
# 3060926299520 140732039489976 140732039490008 140732039490040 3060926299584 [1, 2, 3, [100, 200, 300]]
```

可以看到拷贝后，新的列表地址与列表中各个可变类型元素的地址都发生了改变，不可变类型元素拷贝后地址不变。

![image96](../assets/python1.0/image96.png)

##### 修改 list1[0] 整型元素

```python
list1[0] = 100  # 修改list1[0]整型元素

print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
# 3060924684544 140732039493144 140732039490008 140732039490040 3060924682624 [100, 2, 3, [100, 200, 300]]

print(id(list3), id(list3[0]), id(list3[1]), id(list3[2]), id(list3[3]), list3)
# 3060926299520 140732039489976 140732039490008 140732039490040 3060926299584 [1, 2, 3, [100, 200, 300]]
```

![image97](../assets/python1.0/image97.png)

##### 修改 list[3] 列表元素

```python
list1[3].append(400)  # 修改list1[3]列表元素，向列表中添加新值

print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
# 3060924684544 140732039493144 140732039490008 140732039490040 3060924682624 [100, 2, 3, [100, 200, 300, 400]]

print(id(list3), id(list3[0]), id(list3[1]), id(list3[2]), id(list3[3]), list3)
# 3060926299520 140732039489976 140732039490008 140732039490040 3060926299584 [1, 2, 3, [100, 200, 300]]
```

![image98](../assets/python1.0/image98.png)

### 拷贝的特殊情况

##### 非容器类型（如数字、字符串、和其他“原子”类型的对象）无法拷贝

```python
import copy

var1 = 1
print(id(var1), var1)  # 140732039489976 1

var2 = copy.copy(var1)
print(id(var2), var2)  # 140732039489976 1

var3 = copy.deepcopy(var1)
print(id(var3), var3)  # 140732039489976 1
```

##### 元组变量如果只包含原子类型对象，则不能对其深拷贝

```python
import copy

tuple1 = (1, 2, 3)  # 元组只包含原子类型对象
print(id(tuple1), tuple1)  # 1653947230848 (1, 2, 3)

tuple2 = copy.deepcopy(tuple1)
print(id(tuple2), tuple2)  # 1653947230848 (1, 2, 3)

tuple1 = (1, 2, 3, [])  # 元组不只包含原子类型对象
print(id(tuple1), tuple1)  # 1653947152432 (1, 2, 3, [])

tuple2 = copy.deepcopy(tuple1)
print(id(tuple2), tuple2)  # 1653947148912 (1, 2, 3, [])
```

## 迭代器

迭代是是遍历容器中元素的一种方式，而迭代器是一个可以记住遍历的位置的对象。迭代器对象从容器的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。字符串，列表或元组对象都可用于创建迭代器。

### 可迭代对象

#### 什么是可迭代对象

我们发现大多数容器对象都可以使用 for 语句：

```python
import os

for element in [1, 2, 3]:
    print(element)
for element in (1, 2, 3):
    print(element)
for key in {"one": 1, "two": 2}:
    print(key)
for char in "123":
    print(char)

with open("myfile.txt", "w") as f:
    f.write("H\ne\nl\nl\no\n \nW\no\nr\nl\nd\n")
for line in open("myfile.txt"):
    print(line, end="")
os.remove("myfile.txt")
```

可以直接作用于 for 循环的数据类型有以下几种：

- 容器，如 list 、 tuple 、 dict 、 set 、 str 等。

- generator ，包括生成器和带 yield 的generator function。

这些可以直接作用于 for 循环的对象统称为可迭代对象：Iterable。

#### 判断是否是可迭代对象（Iterable）

```python
from collections.abc import Iterable

print(isinstance([], Iterable))  # True
print(isinstance((), Iterable))  # True
print(isinstance(set(), Iterable))  # True
print(isinstance({}, Iterable))  # True
print(isinstance("100", Iterable))  # True
print(isinstance(100, Iterable))  # False
```

#### 判断是否是迭代器（Iterator）

```python
from collections.abc import Iterator

print(isinstance([], Iterator))  # False
print(isinstance((), Iterator))  # False
print(isinstance(set(), Iterator))  # False
print(isinstance({}, Iterator))  # False
print(isinstance("100", Iterator))  # False
print(isinstance((x for x in range(10)), Iterator))  # True
```

### 使用迭代器

迭代器有两个基本的方法：iter() 和 next()。

在容器对象上使用 for 语句时，在幕后，for 语句会在容器对象上调用 iter()。该函数返回一个定义了 __next__() 方法的迭代器对象，此方法将逐一访问容器中的元素。当元素用尽时，__next__() 将引发 StopIteration 异常来通知终止 for 循环。 你可以使用 next() 内置函数来调用 __next__() 方法。

我们可以使用 iter() 获取一个可迭代对象的迭代器，并使用 next() 遍历迭代器：

```python
list = [1, 2, 3]
it = iter(list)  # 创建迭代器对象
print(next(it))  # 输出迭代器的下一个元素,1
print(next(it))  # 2
print(next(it))  # 3
print(next(it))  # StopIteration
```

也可以使用 for 来遍历迭代器：

```python
list = [1, 2, 3]
it = iter(list)  # 创建迭代器对象
for i in it:
    print(i)
```

### 创建迭代器

了解了迭代器协议背后的机制后，就可以为类添加迭代器行为了。定义 __iter__() 方法用于返回一个带有 __next__() 方法的对象。如果类已定义了 __next__()，那么 __iter__() 可以简单地返回 self。

```python
class Reverse:
    """对一个序列执行反向循环的迭代器。"""

    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

rev = Reverse([2, 3, 5, 7, 11, 13, 17, 19])
iter(rev)
for char in rev:
    print(char)
```

## 生成器

### 什么是生成器

生成器（generator）是一个用于创建迭代器的简单而强大的工具。它的写法类似于标准的函数，但当它要返回数据时会使用 yield 语句。当在生成器函数中使用 yield 语句时，函数的执行将会暂停，并将 yield 后的表达式作为当前迭代的值返回。

每次调用生成器的 next() 方法或使用 for 循环进行迭代时，函数会从上次暂停的地方继续执行（它会记住上次执行语句时的所有数据值），直到再次遇到 yield 语句。这样，生成器函数可以逐步产生值，而不需要一次性计算并返回所有结果。

生成器函数的优势是它们可以按需生成值，避免一次性生成大量数据并占用大量内存。此外，生成器还可以与其他迭代工具（如for循环）无缝配合使用，提供简洁和高效的迭代方式。

### 创建生成器

#### 使用推导式创建生成器

```python
generator = (x for x in range(5))  # 创建生成器
print(generator)  # <generator object <genexpr> at 0x0000026C2066CB80>
for x in generator:
    print(x)
```

#### 使用函数创建生成器

```python
def fibo():  # 斐波那契数列
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b

f = fibo()
print(next(f))  # 1
print(next(f))  # 1
print(next(f))  # 2
print(next(f))  # 3
print(next(f))  # 5
```

如果我们要获取生成器中 return 的值，我们需要捕获 StopIteration异常：

```python
def fibo(n):  # 斐波那契数列
    a, b, counter = 0, 1, 0
    while counter < n:
        yield b
        a, b, counter = b, a + b, counter + 1
    return "done"

f = fibo(10)
try:
    while True:
        print(next(f))
except StopIteration as result:
    print("StopIteration", result)  # StopIteration done
```

### send()

#### 向生成器发送值

恢复执行并向生成器函数“发送”一个值。 这个值作为当前 yield 表达式的结果。 send() 方法会返回生成器所产生的下一个值，或者如果生成器没有产生下一个值就退出则会引发 StopIteration。

使用 send() 发送任务id，使生成器交替执行两个任务：

```python
def gen():
    task_id = 0
    int_value = 0
    char_value = "A"
    while True:
        # task_id 为 0 则 int_value +1，task_id 为 1 则 char_value +1
        match task_id:
            case 0:
                task_id = yield int_value  # 返回 int_value，并接收 send() 发送来的值给 task_id
                int_value += 1
            case 1:
                task_id = yield char_value  # 返回 char_value，并接收 send() 发送来的值给 task_id
                char_value = chr(ord(char_value) + 1)
            case _:
                task_id = yield  # 返回 None

g = gen()
print(next(g))  # 0
print(g.send(1))  # A
print(g.send(0))  # 1
print(g.send(1))  # B
print(g.send(0))  # 2
```

#### 使用 send(None) 启动生成器

当调用 send() 来启动生成器时，它必须以 None 作为调用参数，因为这时没有可以接收值的 yield 表达式。

```python
def gen():
    task_id = 0
    int_value = 0
    char_value = "A"
    while True:
        # task_id 为 0 则 int_value +1，task_id 为 1 则 char_value +1
        match task_id:
            case 0:
                task_id = yield int_value  # 返回 int_value，并接收 send() 发送来的值给 task_id
                int_value += 1
            case 1:
                task_id = yield char_value  # 返回 char_value，并接收 send() 发送来的值给 task_id
                char_value = chr(ord(char_value) + 1)
            case _:
                task_id = yield  # 返回 None

g = gen()
print(g.send(None))  # 0
print(g.send(1))  # A
print(g.send(0))  # 1
```

## 命名空间

### 什么是命名空间

命名空间（Namespace）是从名称到对象的映射，现在，大多数命名空间都使用Python字典实现。各个命名空间是独立的，没有任何关系的，所以一个命名空间中不能有重名，但不同的命名空间是可以重名而没有任何影响。

### 三种命名空间

一般有三种命名空间，在不同时刻创建，且拥有不同的生命周期：

#### 内置名称

内置名称的命名空间是在 Python 解释器启动时创建的，永远不会被删除。

#### 一个模块的全局名称

模块的全局命名空间在读取模块定义时创建。通常，模块的命名空间也会持续到解释器退出。

从脚本文件读取或交互式读取的，由解释器顶层调用执行的语句，是 __main__ 模块调用的一部分，也拥有自己的全局命名空间。

内置名称实际上也在模块里，即 builtins。

#### 一个函数调用中的局部名称

函数的局部命名空间在函数被调用时被创建，并在函数返回或抛出未在函数内被处理的异常时被删除（实际上，用“遗忘”来描述实际发生的情况会更好一些）。当然，每次递归调用都有自己的局部命名空间。

## 作用域

### 什么是作用域

一个命名空间的作用域是Python代码中的一段文本区域，从这个区域可直接访问该命名空间。

### 四种作用域

- 最内层作用域（Local），包含局部名称，并首先在其中进行搜索

- 那些外层闭包函数的作用域（Enclosing）：包含“非局部、非全局”的名称，从最靠内层的那个作用域开始，逐层向外搜索。

- 倒数第二层作用域（Global）：包含当前模块的全局名称

- 最外层（最后搜索）的作用域（Built-in）：是内置名称的命名空间

global 语句用于表明特定变量在全局作用域里，并应在全局作用域中重新绑定。

nonlocal 语句表明特定变量在外层作用域中，并应在外层作用域中重新绑定。

在最内层作用域访问全局作用域或外层作用域的变量时，若不使用 global 或 nonlocal 语句，这些变量将为只读，尝试写入这样的变量将在最内层作用域中创建一个新的局部变量，而使得同名的外部变量保持不变。

![image99](../assets/python1.0/image99.png)

## 闭包

### 什么是闭包

当调用的函数执行完毕后，函数内的变量就会被销毁。但有时希望在调用函数后函数内的数据能够保存下来重复使用，这时候可以用到闭包。闭包可以避免使用全局值，并提供某种形式的数据隐藏。

构建闭包的条件：

- 外部函数内定义一个内部函数。

- 内部函数用到外部函数中的变量。

- 外部函数将内部函数作为返回值。

### 使用闭包

```python
# 构建闭包
def linear(a, b):
    def inner(x):
        return a * x + b

    return inner

y1 = linear(1, 1)
print(y1)  # <function linear.<locals>.inner at 0x00000291279D19E0>
print(y1(5))  # 6
```

将调用 linear() 后返回的函数对象赋值给 y1，虽然 linear() 函数已经执行完毕，但是我们调用 y1() 时，y1() 仍然记得 linear() 中 a 和 b 的值。

### 查看闭包中的值

所有函数对象都有一个 __closure__ 属性，如果它是一个闭包函数，则该属性返回单元格对象的元组，每个单元格对象都对应着闭包所引用的外部函数作用域中的一个变量。对于普通函数，__closure__ 属性的值通常为 None。

```python
def linear(a, b):
    def inner(x):
        return a * x + b

    return inner

y1 = linear(1, 2)
objects = y1.__closure__
print(objects)
print(objects[0].cell_contents)  # 1
print(objects[1].cell_contents)  # 2
```

## 装饰器

### 什么是装饰器

装饰器允许在不修改原有函数代码的基础上，动态地增加或修改函数的功能。装饰器本质上是一个接收函数作为输入并返回一个新的包装过后的函数的对象。

### 使用装饰器

#### 语法

```python
def decorator(func):
    def inner(参数):
        # 添加功能
        func(参数)
        # 添加功能

    return inner
```

decorator 是一个装饰器函数，它接受一个函数 func 作为参数，并返回一个内部函数 inner。在 inner 函数内部，我们可以执行一些额外的操作，然后调用原始函数 func，并返回其结果。

#### 闭包实现装饰器

```python
from math import sqrt

def func(x):
    """开根号"""
    return sqrt(x)

def decorator(f):
    def inner(x):
        x = abs(x)  # 求x的绝对值
        return f(x)

    return inner

func = decorator(func)
print(func(-4))  # 2.0
```

#### @decorator使用装饰器

当我们使用 @decorator 前缀在 func 定义前，Python会自动将 func 作为参数传递给 decorator，然后将返回的 inner 函数替换掉原来的 func。

```python
from math import sqrt

def decorator(f):
    def inner(x):
        x = abs(x)  # 求x的绝对值
        return f(x)

    return inner

@decorator
def func(x):
    """开根号"""
    return sqrt(x)

print(func(-4))  # 2.0
```

### 多层装饰器

多个装饰器的装饰过程：离函数最近的装饰器先装饰，然后外面的装饰器再进行装饰。

```python
from math import sqrt

# 将参数转化为整型
def get_integer(f):
    def inner(x):
        x = int(x)
        return f(x)

    return inner

# 将参数转换为非负数
def get_absolute(f):
    def inner(x):
        x = abs(x)
        return f(x)

    return inner

@get_integer
@get_absolute
def func(x):
    """开根号"""
    return sqrt(x)

print(func("-4"))  # 2.0
```

### 带参数的装饰器

```python
from math import sqrt

# 求根号n次
def times(n):
    # 将参数转换为非负数
    def get_absolute(f):
        def inner(x):
            x = abs(x)
            for i in range(n):
                x = f(x)
            return x

        return inner

    return get_absolute

@times(2)
def func(x):
    """开根号"""
    return sqrt(x)

print(func(-16))  # 2.0
```

### 类装饰器

- 类装饰器是包含 __call__() 方法的类，它接受函数作为参数，并返回新的函数。

```python
from math import sqrt

class DecoratorClass:
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        x = abs(x)
        return self.f(x)

@DecoratorClass
def func(x):
    """开根号"""
    return sqrt(x)

print(func(-4))  # 2.0
```
