# SQLAlchemy

## ORM介绍

### 什么是 ORM

ORM（Object-Relational Mapping，对象关系映射）是一种编程技术，它将数据库中的表结构映射为编程语言中的类，将表中的行映射为类中的对象，让开发者可以用面向对象的方式操作数据库，而无需直接编写 SQL 语句。

### ORM的核心价值

- 屏蔽数据库差异
同一套代码可适配多种数据库（MySQL、PostgreSQL 等），无需修改核心逻辑。

- 简化开发流程
用类、对象、方法替代 SQL 语句，降低数据库操作的学习成本。

- 提高代码可读性
将数据库操作与业务逻辑融合，代码更符合面向对象思维。

- 自动处理类型转换
无需手动转换数据库字段与Python类型（如MySQL的INT与Python的int）。

### 主流ORM产品对比

Python生态中有多个成熟的ORM工具，各有侧重，以下是常见产品的对比：

| ORM工具 | 特点 | 适用场景 |
| --- | --- | --- |
| SQLAlchemy | 功能全面，支持ORM和原生SQL，灵活度极高，文档丰富，生态完善。 | 中大型项目、复杂查询场景、需要跨数据库兼容。 |
| Django ORM | 与 Django 框架深度绑定，开箱即用，简化 CRUD 操作，但灵活性较低。 | Django 框架开发的 Web 应用。 |
| Tortoise-ORM | 异步 ORM，支持 async/await，与 FastAPI 等异步框架契合度高。 | 异步 Web 应用（如 FastAPI + 异步数据库驱动）。 |
| SQLModel | 基于 SQLAlchemy 和 Pydantic，简化模型定义，兼顾 ORM 和数据验证。 | FastAPI 项目，追求模型定义简洁性。 |

SQLAlchemy是Python中最成熟的ORM 之一，既支持简单的CRUD 操作，也能应对复杂的多表关联、事务管理等场景，且与FastAPI兼容性极佳，是生产环境的首选。

## SQLAlchemy基本架构

![示例截图](assets/image14.png)

SQLAlchemy的架构分层，从下到上可分为DBAPI 层、SQLAlchemy Core（核心层）、SQLAlchemy ORM（对象关系映射层），各组件作用如下：

### DBAPI（数据库通信层）

DBAPI（Database API）是Python数据库接口规范，是SQLAlchemy与底层数据库通信的 “桥梁”。

不同数据库（如 MySQL、PostgreSQL）有各自的 DBAPI 实现（如 pymysql 是 MySQL 的 DBAPI，psycopg2 是 PostgreSQL 的 DBAPI）。SQLAlchemy 通过适配这些 DBAPI，实现对多种数据库的兼容。

### SQLAlchemy Core（核心层）

Core是SQLAlchemy的 “基础工具集”，提供了SQL表达式语言、数据库连接管理等核心能力，即使不使用 ORM，也能通过 Core 操作数据库。

##### Schema / Types

定义数据库的模式（Schema）和数据类型（Types）。

Schema对应数据库的表、列、约束等结构（比如定义一张表有哪些字段、字段类型是什么）。Types封装了数据库支持的数据类型（如 Integer、String、DateTime 等），并提供 Python 类型与数据库类型的映射。

##### SQL Expression Language

用Python代码生成SQL语句的 “表达式语言”。

它允许你用面向对象的方式编写 SQL（比如用 table.c.column == value 表示 WHERE column = value），既保留了 SQL 的灵活性，又能避免手写 SQL 带来的语法错误和安全问题（如 SQL 注入）。

##### Engine

管理数据库连接的 “引擎”，是与数据库交互的 “入口”。

Engine 负责创建和维护数据库连接，还会集成连接池（Connection Pooling）和方言（Dialect）。

##### Connection Pooling

管理数据库连接池，提升数据库操作性能。

连接池会预先创建一批数据库连接并复用，避免频繁创建 / 销毁连接的开销，尤其在高并发场景下能显著提高效率。

##### Dialect

处理 “方言” 差异，适配不同数据库的 SQL 语法和特性。

不同数据库（如 MySQL 和 PostgreSQL）的 SQL 语法、函数可能有差异（比如 MySQL 的 LIMIT 和 PostgreSQL 的 LIMIT/OFFSET 用法不同）。Dialect 会对这些差异做 “翻译”，让上层代码能以统一的方式操作不同数据库。

### SQLAlchemy ORM（对象关系映射层）

在Core的基础上，提供象关系映射（ORM）能力，让开发者可以用 “类和对象” 的方式操作数据库（比如用 User 类对应 users 表，用 user = User(name="Alice") 表示新增一条用户记录）。

ORM本质是对Core的 “封装”—— 它会把面向对象的操作（如创建对象、查询对象）自动转换为Core能理解的 SQL 表达式通过，最终 Engine 执行。这样开发者可以更聚焦于业务逻辑，而无需关注底层SQL实现。

### 核心组件

- 引擎（Engine）
Engine 是与数据库的连接入口，负责管理连接池和执行 SQL 语句。

- 基类（Base）
所有 ORM 模型的父类，用于统一管理数据库表结构。

- 会话（Session）
用于执行数据库操作的会话对象，负责暂存、提交、回滚数据操作。

## 环境准备

### 安装依赖

```bash
# 安装 SQLAlchemy 核心库
pip install sqlalchemy

# 安装 MySQL 驱动（推荐 pymysql，兼容 Python 3.x）
pip install pymysql
```

### 准备 MySQL 环境

确保本地或远程 MySQL 服务已启动（默认端口 3306）。

创建一个测试数据库（如 fastapi_db）

## 基本操作案例

### 在base.py中定义Base基类

```python
from sqlalchemy.ext.declarative import declarative_base

# 生成基类，所有模型需继承该类
Base = declarative_base()
```

### 在models.py中定义ORM模型类（映射MySQL表）

模型类在定义的时候需要继承Base基类。

模型类对应MySQL中的表，类属性对应表字段，通过 Column 定义字段类型和约束。

```python
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from demo.base import Base

class Department(Base):
    """部门模型（一对多：一个部门包含多个员工）"""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # 部门名称
    location = Column(String(100))  # 部门位置（如"北京总部"）

    # 一对多关联员工：返回员工列表，显式指定外键（可选，但更清晰）
    employees = relationship(
        "Employee",
        back_populates="department",
        # 可选：级联删除（删除部门时自动删除下属员工，根据业务选择）
        # cascade="all, delete-orphan",
        # 可选：懒加载策略，优化查询性能
        lazy="selectin"
    )

class Employee(Base):
    """员工模型（多对一：多个员工属于一个部门）"""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # 姓名
    age = Column(Integer)  # 年龄
    hire_date = Column(Date)  # 入职日期

    #添加外键约束，绑定到departments.id
    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="RESTRICT"),  # 禁止删除有员工的部门
        nullable=False  # 员工必须归属一个部门（根据业务可改为True，允许无部门）
    )

    # 核心修正：多对一关联，指定uselist=False（返回单个部门对象）
    department = relationship(
        "Department",
        back_populates="employees",
        lazy="joined"  # 可选：立即加载部门数据，减少查询次数
    )
```

字段约束说明：

- primary_key=True：设为主键。
- autoincrement=True：MySQL 自增（仅整数类型可用）。
- unique=True：唯一索引，避免重复值。
- nullable=False：非空约束（字段必须有值）。
### 在database.py创建引擎以及会话

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL 连接格式：mysql+pymysql://用户名:密码@主机地址:端口/数据库名
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/fastapi_db"

# 创建引擎（echo=True 会打印执行的 SQL，方便调试）
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 是否启用日志输出 开发环境启用，生产环境关闭
    pool_pre_ping=True  # 连接前检查有效性，避免连接失效
)

# 创建会话工厂（绑定引擎）
SessionLocal = sessionmaker(
    autocommit=False,  # 关闭自动提交，需手动 commit()
    bind=engine
)
```

autoflush=False ：SQLAlchemy 的会话（Session）内部维护了一个 “身份映射”（Identity Map），用于缓存当前会话中操作的对象。当你执行 db.add(new_user) 时，new_user 仅被添加到这个会话内存的缓存中，并未同步到数据库（无论是缓冲区还是物理表）。

### 在main.py中提供建表方法

创建表结构，通过基类的 create_all 方法在 MySQL 中创建表（仅需执行一次）

```python
from demo.base import Base
from demo.database import engine
from demo.models import Employee,Department #必须要加

# 创建表
def create_table():
    print("注册的表名:", Base.metadata.tables.keys())
    # 创建所有模型对应的表
    Base.metadata.create_all(bind=engine)
    print("表创建成功")

if __name__ == '__main__':
    create_table()
```

执行后，MySQL 中会生成 employees 和 departments表，包含定义的字段和约束。

### 新增数据（Create）

```python
def insert_data():
    # 获取数据库会话
    db = SessionLocal()

    try:
        # =========== 第一步：新增部门 =============
        new_dept = Department(
            name="研发部",  # 部门名称（唯一）
            location="北京总部"  # 部门位置
        )
        db.add(new_dept)  # 将部门对象加入会话
        db.commit()  # 提交到数据库（执行 INSERT 语句）
        db.refresh(new_dept)  # 刷新对象，获取自增的 id 等字段

        # =========== 第二步：新增关联的员工 ===========
        # 员工1：关联上面创建的研发部
        emp1 = Employee(
            name="张三",
            age=30,
            hire_date=date(2023, 1, 1),  # 入职日期（datetime.date 类型）
            department_id=new_dept.id  # 关联部门 ID（外键）
        )
        # 员工2：同部门的另一个员工
        emp2 = Employee(
            name="李四",
            age=28,
            hire_date=date(2023, 3, 15),
            department_id=new_dept.id
        )

        # 批量添加员工（也可逐个 add）
        db.add_all([emp1, emp2])
        db.commit()  # 提交员工数据
        # 刷新员工对象，获取自增 ID
        db.refresh(emp1)
        db.refresh(emp2)

        # ===================== 输出结果 =====================
        print(f"新增部门：ID={new_dept.id}，名称={new_dept.name}，位置={new_dept.location}")
        print(f"新增员工1：ID={emp1.id}，姓名={emp1.name}，所属部门={new_dept.name}")
        print(f"新增员工2：ID={emp2.id}，姓名={emp2.name}，所属部门={new_dept.name}")

        # 验证关联关系（通过 ORM 关联查询）
        print("\n【验证关联关系】")
        # 从员工查部门
        print(f"员工{emp1.name}的部门名称：{emp1.department.name}")
        # 从部门查员工
        dept_employees = new_dept.employees
        print(f"部门{new_dept.name}的员工列表：{[emp.name for emp in dept_employees]}")

    except Exception as e:
        db.rollback()  # 出错时回滚
        print(f"新增失败：{e}")
    finally:
        db.close()  # 关闭会话
```

### 删除数据（Delete）

```python
def delete_data():
    # 获取会话
    session = SessionLocal()

    try:
        # 删除单个员工
        emp = session.query(Employee).filter(Employee.name == "李四").first()
        if emp:
            session.delete(emp)
            session.commit()
            print(f"已删除员工：{emp.name}")

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"刪除失败：{e}")
    finally:
        session.close()  # 关闭会话
```

### 修改数据（Update）

```python
def update_data():
    # 获取会话
    session = SessionLocal()
    try:
        # 修改员工年龄
        emp = session.query(Employee).filter(Employee.name == "张三").first()
        if emp:
            emp.age = 31  # 直接修改属性
            session.commit()  # 提交更新
            print(f"修改后 {emp.name} 的年龄：{emp.age}")

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"修改失败：{e}")
    finally:
        session.close()  # 关闭会话
```

### 查询数据（Read）

```python
def read_data():
    # 获取会话
    session = SessionLocal()
    try:
        # ======按主键查询 get========
        #  查询id=1的部门
        dept = session.get(Department,1)
        print(f"部门 ID=1：{dept.name}（{dept.location}）")

        # ======过滤（filter）查询========
        # 查询研发部的所有员工
        rd_employees = session.query(Employee).filter(
            Employee.department_id == 1  # 按部门ID过滤
        ).all()
        print("研发部员工：", [emp.name for emp in rd_employees])  # 输出：['张三']

        # 查询年龄>30的员工
        old_employees = session.query(Employee).filter(Employee.age > 30).all()
        print("年龄>30的员工：", [emp.name for emp in old_employees])  # 输出：['张三', '王五']

        # ======逻辑运算（and_/or_）查询========
        from sqlalchemy import and_, or_

        # 年龄30-40且属于研发部的员工（and_）
        emp = session.query(Employee).filter(
            and_(Employee.age.between(30, 40), Employee.department_id == 1)
        ).first()
        print("符合条件的员工：", emp.name)  # 输出：张三

        # 属于市场部或年龄>32的员工（or_）
        emps = session.query(Employee).filter(
            or_(Employee.department_id == 2, Employee.age > 32)
        ).all()
        print("符合条件的员工：", [emp.name for emp in emps])  # 输出：['张三', '王五']

        # ======表连接（join）查询========
        # 内连接：查询员工及其所属部门名称
        # 语法：query(主表, 关联表).join(关联表, 连接条件)
        result = session.query(Employee, Department).join(
            Department, Employee.department_id == Department.id
        ).all()

        for emp, dept in result:
            print(f"员工 {emp.name} 属于 {dept.name}")
        # 输出：
        # 员工 张三 属于 研发部
        # 员工 王五 属于 市场部

        # ======预加载关联数据（joinedload）查询========
        from sqlalchemy.orm import joinedload

        # 加载员工时同时加载部门信息（避免多次查询）
        employees = session.query(Employee).options(
            joinedload(Employee.department)  # 预加载关联的 department
        ).all()

        # 直接访问关联数据，不会触发新查询
        for emp in employees:
            print(f"{emp.name} 的部门：{emp.department.name}")
        # 输出：
        # 张三 的部门：研发部
        # 王五 的部门：市场部

        # ======子查询（subquery）========
        from sqlalchemy import func
        #子查询：统计每个部门的员工数，再查询员工数>0的部门
        # 步骤1：创建子查询（统计部门员工数）
        dept_emp_count = session.query(
            Employee.department_id,
            func.count(Employee.id).label("count")  # 别名 count
        ).group_by(Employee.department_id).subquery()  # 转为子查询

        # 步骤2：主查询（关联子查询结果）
        depts = session.query(Department).join(
            dept_emp_count, Department.id == dept_emp_count.c.department_id
        ).filter(dept_emp_count.c.count > 0).all()  # 筛选员工数>0的部门

        print("有员工的部门：", [dept.name for dept in depts])  # 输出：['研发部', '市场部']

        # ======去重（distinct）========
        # 查询所有有员工的部门位置（去重）
        locations = session.query(Department.location).join(
            Employee
        ).distinct().all()  # distinct() 去重

        print("部门位置：", [loc[0] for loc in locations])  # 输出：['北京', '广州']

        # ======结果获取（first/all）========
        # first()：返回第一条结果（适合唯一查询）
        first_emp = session.query(Employee).first()
        print("第一个员工：", first_emp.name)  # 输出：张三

        # all()：返回所有结果（列表）
        all_depts = session.query(Department).all()
        print("所有部门：", [dept.name for dept in all_depts])  # 输出：['研发部', '市场部']

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话
```

## 关联关系

在 SQLAlchemy 中，关联关系（Relationship） 用于定义不同模型（表）之间的业务关联（如一对一、一对多、多对多），通过 relationship 函数实现，配合字段定义（如外键）可实现对象化的关联查询和操作。

### 常见的关联关系

关联关系本质是映射数据库中表与表的关系，SQLAlchemy 提供了 4 种基础关联类型：

| 关联类型 | 场景示例 | 数据库实现 |
| --- | --- | --- |
| 一对多（One-to-Many） | 一个用户拥有多个商品 | 子表通过外键关联主表 |
| 多对一（Many-to-One） | 多个商品属于一个用户 | 同上（一对多的反向视角） |
| 一对一（One-to-One） | 一个用户对应一个个人资料 | 子表外键设为唯一（unique=True） |
| 多对多（Many-to-Many） | 多个学生选修多个课程 | 通过中间表关联两个表 |

### 核心配置参数（relationship 函数）

relationship 函数是定义关联关系的核心，常用参数如下

| 参数 | 作用 | 示例 |
| --- | --- | --- |
| argument | 必选，指定关联的目标模型（类或字符串） | relationship("Item") |
| back_populates | 双向关联时，指定反向关联的字段名（显式定义双向关系） | back_populates="owner" |
| backref | 简化双向关联，自动为目标模型添加反向关联字段（隐式定义） | backref="owner" |
| foreign_keys | 显式指定关联的外键字段（多外键场景下必用） | foreign_keys=[Item.owner_id] |
| cascade | 级联操作规则（如保存、删除关联数据） | cascade="all, delete-orphan" |
| lazy | 关联数据的加载方式（控制查询性能） | lazy="selectin"（一次性加载） |
| uselist | 控制是否为集合（True 表示一对多，False 表示一对一） | uselist=False（一对一） |
| secondary | 多对多关系中，指定中间表 | secondary=user_course |
| primaryjoin/secondaryjoin | 复杂关联时，显式定义表连接条件（默认自动生成） | primaryjoin=(User.id == Item.owner_id) |

### 具体关联类型的配置方式

#### 一对多（One-to-Many）与多对一（Many-to-One）

最常用的关联类型，以 “用户（User）- 商品（Item）” 为例：

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))

    # 一对多：用户拥有多个商品（通过 back_populates 与 Item.owner 双向关联）
    items = relationship(
        "Item",  # 关联目标模型
        back_populates="owner",  # 反向关联字段（Item 中的 owner）
        lazy="selectin",  # 加载方式：查询用户时同时加载商品
        cascade="save-update"  # 级联保存：保存用户时自动保存关联商品
    )

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    owner_id = Column(Integer, ForeignKey("users.id"))  # 外键关联用户表

    # 多对一：商品属于一个用户（反向关联）
    owner = relationship(
        "User",  # 关联目标模型
        back_populates="items"  # 反向关联字段（User 中的 items）
    )
```

使用示例

```python
# 获取会话
session = SessionLocal()
# 创建用户和商品
user = User(username="test")
item = Item(title="商品1", owner=user)  # 直接关联用户
user.items.append(item)  # 或通过用户的 items 列表添加

session.add(user)
session.commit()

# 查询关联数据
user = session.query(User).first()
print(user.items)  # 获取用户的所有商品（因 lazy="selectin" 已加载）

item = session.query(Item).first()
print(item.owner.username)  # 获取商品所属用户的用户名
```

#### 一对一（One-to-One）

在一对多基础上，通过 uselist=False 限制关联为单个对象，以 “用户（User）- 个人资料（Profile）” 为例：

```python
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))

    # 一对一：用户对应一个资料（uselist=False 表示非集合）
    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,  # 关键：关联结果为单个对象（非列表）
        cascade="all, delete-orphan"  # 删除用户时删除资料
    )

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    bio = Column(String(200))  # 个人简介
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # 外键唯一

    # 反向关联用户
    user = relationship("User", back_populates="profile")
```

关键点：

- 子表（Profile）的外键需设 unique=True，确保一个用户只对应一个资料；
- 主表（User）的 relationship 需设 uselist=False，表示关联结果是单个对象（而非列表）。
使用示例

```python
# 获取会话
session = SessionLocal()
# 方式1：先创建用户，再创建资料并关联
user1 = User(username="alice")
session.add(user1)
session.commit()  # 先提交用户，获取 ID

profile1 = Profile(bio="喜欢读书", user_id=user1.id)  # 通过 user_id 关联
session.add(profile1)
session.commit()

# 方式2：直接通过 relationship 关联（更简洁）
user2 = User(
    username="bob",
    profile=Profile(bio="热爱运动")  # 直接嵌套 Profile 对象
)
session.add(user2)
session.commit()  # 自动同步 user_id
```

#### 多对多（Many-to-Many）

需要通过中间表关联两个模型，以 “学生（Student）- 课程（Course）” 为例：

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

from sqlalchemy import Table  # 用于定义中间表

# 1. 定义中间表（无需模型类，直接用 Table 定义）
student_course = Table(
    "student_course",  # 中间表名
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # 多对多：学生选修多个课程（通过 secondary 指定中间表）
    courses = relationship(
        "Course",
        secondary=student_course,  # 关联中间表
        back_populates="students",
        lazy="selectin"
)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    # 反向关联：课程包含多个学生
    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )
```

使用示例：

```python
# 获取会话
session = SessionLocal()
# 创建学生和课程
student1 = Student(name="张三")
student2 = Student(name="李四")
course1 = Course(name="数学")
course2 = Course(name="英语")

# 建立关联
student1.courses = [course1, course2]
student2.courses = [course1]

session.add_all([student1, student2, course1, course2])
session.commit()

# 查询：学生选修的课程
print(student1.courses)  # [Course(name="数学"), Course(name="英语")]

# 查询：课程包含的学生
print(course1.students)  # [Student(name="张三"), Student(name="李四")]
```

### 关键参数详解

#### 双向关联：back_populates vs backref

- back_populates（推荐）：显式在两个模型中定义反向关联，逻辑清晰。
例：User.items 设 back_populates="owner"，Item.owner 设 back_populates="items"。

- backref：简化写法，在一个模型中定义即可自动为另一个模型生成反向字段。
例：User.items = relationship("Item", backref="owner")，则 Item 会自动拥有 owner 字段。

#### 级联操作（cascade）

控制主对象操作对关联对象的影响，常用规则：

- save-update：保存主对象时自动保存关联对象（默认值）；
- delete：删除主对象时自动删除关联对象；
- delete-orphan：关联对象与主对象解除关联时自动删除（仅用于一对多）；
- all：包含 save-update, merge, refresh-expire, expunge, delete。
例：cascade="all, delete-orphan" 表示 “全量级联 + 解除关联时删除”。

#### 加载方式（lazy）

控制关联数据的查询时机，影响性能：

- select（默认）：访问关联属性时才查询（可能产生 N+1 问题）；
- selectin：查询主对象时，通过 IN 语句一次性加载所有关联数据（推荐）；
- joined：通过 JOIN 语句与主对象一起加载（适合一对一）；
- subquery：通过子查询加载关联数据；
- dynamic：返回查询对象（可继续添加过滤条件，适合大数据量）。
### 总结

- 关联关系是 SQLAlchemy ORM 的核心，通过 relationship 函数定义，配合外键或中间表实现；
- 按业务场景选择关联类型（一对多、一对一、多对多），并配置双向关联（back_populates）；
- 合理设置 cascade（级联）和 lazy（加载方式），平衡代码简洁性和性能；
- 多对多关系需通过中间表（Table 实例）实现，无需定义模型类。
## sqlacodegen通过表生成类

sqlacodegen 是一个实用工具，能根据现有数据库表结构（或 SQL 语句）自动生成 SQLAlchemy 模型类，省去手动编写模型的麻烦，尤其适合已有数据库的项目迁移。

它支持多种数据库（MySQL、PostgreSQL、SQLite 等），生成的模型类包含表名、字段类型、主键、外键、索引等完整信息。

### 安装依赖

```bash
# 直接安装（支持 SQLAlchemy 1.4+ 和 2.0+）
pip install sqlacodegen

# 如果需要连接特定数据库，需安装对应驱动（以 MySQL 为例）
pip install pymysql  # MySQL 驱动
```

### 准备数据库表（SQL）

先在数据库中创建 departments（部门）和 employees（员工）表，包含一对多关系（一个部门有多个员工）：

```sql
-- 部门表
CREATE TABLE departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '部门名称',
    location VARCHAR(100) COMMENT '部门位置',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 员工表（关联部门）
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '员工姓名',
    age INT COMMENT '年龄',
    hire_date DATE COMMENT '入职日期',
    department_id INT COMMENT '所属部门ID',
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    INDEX idx_dept (department_id)  -- 部门索引，优化查询
);
```

### 创建table_2_models.py用于接收创建的模型类

### 在gen.py中进行测试

```python

import subprocess
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from demo1.table_2_models import Departments, Employees

# 创建数据库引擎
db_host = "localhost"
db_port = 3306
db_name = "fastapi_db"
db_user_name = "root"
db_password = "123456"
url = f"mysql+pymysql://{db_user_name}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
engine = create_engine(url, echo=True)

# 配置会话工厂
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 生成模型类
def table_2_model(run=False):
    """将数据库表映射为Python类"""
    if not run:
        return
    output_path = "table_2_models.py"

    venv_python = sys.executable  # 若PyCharm使用虚拟环境，这里会返回.venv下的python.exe
    print("当前使用的Python路径：", venv_python)  # 确认输出是.venv/Scripts/python.exe

    cmd = [venv_python, "-m", "sqlacodegen", url]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    # 打印执行结果（定位问题核心）
    print("=== 命令执行结果 ===")
    print(f"返回码（0=成功，非0=失败）：{result.returncode}")
    print(f"标准输出：\n{result.stdout}")
    print(f"错误输出：\n{result.stderr}")  # 重点看这里，会显示失败原因

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.stdout)

# 向员工和部门表中插入数据
def insert_dept_emp():
    # 1. 创建员工对象（用关键字参数，日期转换为date类型）
    emp = Employees(
        id=100,  # 显式指定参数名
        name='zs',
        age=20,
        # hire_date=date(2025, 10, 10)  # 字符串转date对象
        hire_date='2025-10-10'  # 字符串转date对象
    )

    # 2. 创建部门对象（关键字参数，日期转换为datetime类型）
    dept = Departments(
        id=10,
        name='研发部',
        location='北京',
        created_at='2025-10-10',  # 字符串转datetime对象
        employees=[emp]  # 关联员工
    )

    # 3. 插入数据库
    with Session(engine) as session:
        session.add(dept)
        try:
            session.commit()
            print(f"插入成功！部门ID：{dept.id}，员工ID：{emp.id}")
        except Exception as e:
            session.rollback()
            print(f"插入失败：{e}")
if __name__ == "__main__":
    # table_2_model(True)
    insert_dept_emp()
```
