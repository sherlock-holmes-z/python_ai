<!-- 文件说明：作为项目统一入口，解释架构职责、启动方式和验证命令，减少跨电脑运行时的隐含知识。 -->

# FastAPI + MySQL + PostgreSQL + Redis CRUD

这是一个 Python 3.12、FastAPI、SQLAlchemy 2.x 异步 ORM 示例：MySQL 保存商品主数据，Redis 缓存商品详情，PostgreSQL 保存操作审计日志。

## 项目结构

```text
04_orm/
├── app/
│   ├── api/              # 路由和 Depends 依赖
│   ├── core/             # 配置和领域异常
│   ├── db/               # MySQL/PostgreSQL/Redis 连接
│   ├── models/           # SQLAlchemy ORM 模型
│   ├── repositories/     # 单数据源持久化
│   ├── schemas/          # Pydantic 请求/响应模型
│   ├── services/         # 跨存储业务编排
│   └── main.py           # FastAPI 应用入口
├── docs/                 # ADR 和领域模型
├── redis/                # Redis 初始化命令
├── sql/                  # MySQL/PostgreSQL 初始化脚本
└── tests/                # 不访问外部服务的测试
```

## 1. 安装后端依赖

在仓库根目录执行：

```powershell
conda activate python-ai
python -m pip install -e ".[dev,backend]"
```

## 2. 准备本地配置

进入本目录并复制配置模板：

```powershell
Set-Location "D:\code\python\python_ai\src\fastapi\fastapi\04_orm"
Copy-Item .env.example .env
```

编辑 `.env`，把 MySQL/PostgreSQL 密码占位符替换为真实密码。Redis 没有密码时保持空值。

## 3. 初始化 MySQL

先修改 `sql/mysql/00_init.sql` 中的密码占位符，再使用管理员账号执行：

```powershell
cmd /c "mysql -h 192.168.100.102 -P 3306 -u root -p < sql\mysql\00_init.sql"
```

脚本会创建数据库、最小权限应用账号、`products` 表并插入两条商品数据。

## 4. 初始化 PostgreSQL

先修改 `sql/postgresql/00_create_database.sql` 中的密码占位符：

```powershell
psql -h 192.168.100.102 -p 5432 -U postgres -f sql/postgresql/00_create_database.sql
psql -h 192.168.100.102 -p 5432 -U fastapi_app -d fastapi_orm -f sql/postgresql/01_schema_seed.sql
```

第一个脚本创建角色和数据库；第二个脚本创建 `product_audit_logs` 并插入初始化审计数据。

## 5. 初始化 Redis

Redis 没有建库、建表语句。连接后逐行执行 `redis/init.redis`：

```powershell
redis-cli -h 192.168.100.102 -p 6379
```

如果 Redis 配置了密码，连接后先执行：

```text
AUTH 你的Redis密码
```

## 6. 启动应用

必须在 `04_orm` 目录执行：

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

打开接口文档：<http://127.0.0.1:8000/docs>

## API

| 方法 | 路径 | 作用 |
| --- | --- | --- |
| `GET` | `/health` | 检查 MySQL、PostgreSQL、Redis |
| `POST` | `/api/v1/products` | 创建商品 |
| `GET` | `/api/v1/products` | 分页查询商品 |
| `GET` | `/api/v1/products/{id}` | 查询商品并使用 Redis 缓存 |
| `PATCH` | `/api/v1/products/{id}` | 局部修改商品并删除缓存 |
| `DELETE` | `/api/v1/products/{id}` | 删除商品并删除缓存 |

创建商品请求示例：

```json
{
  "sku": "BOOK-FASTAPI-001",
  "name": "FastAPI 企业开发",
  "description": "FastAPI、SQLAlchemy 与 Redis",
  "price": 108.00,
  "stock": 30
}
```

## 一致性说明

本示例不实现跨 MySQL/PostgreSQL 的分布式事务。MySQL 商品事务提交后，Redis 和 PostgreSQL 故障不会回滚商品操作。生产环境要求审计不丢失时，应使用 MySQL Outbox + 消息队列，而不是直接跨库双写。详细决策见 `docs/adr-001-storage-responsibilities.md`。
