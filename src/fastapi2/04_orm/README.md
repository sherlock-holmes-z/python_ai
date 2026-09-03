# FastAPI + SQLAlchemy 客服工单 Demo

这是一个面向企业项目结构的教学示例：MySQL 保存客服工单主表和沟通消息子表，FastAPI 提供异步 CRUD、分页和一对多关联查询。

## 1. 为什么这样分层

```text
HTTP 请求
  -> api/routes       参数、状态码、响应模型
  -> services         业务规则、事务边界
  -> repositories     SQLAlchemy 查询和持久化
  -> models            数据表映射
  -> MySQL
```

- 路由层不直接写 SQL，避免接口代码同时承担协议、业务和数据访问三种职责。
- Service 使用 `async with session.begin()` 控制完整事务；失败会自动回滚。
- Repository 不调用 `commit()`，防止一个业务用例执行到一半就永久写入。
- ORM Model 和 Pydantic Schema 分开，客户端不能随意写入主键、工单编号和时间戳。
- 工单详情使用 `selectinload` 主动加载消息，适合一对多，也避免异步 ORM 懒加载报错。

更详细的业务规则见 [领域模型](docs/01_domain_model.md)，技术选型见 [ADR-0001](docs/adr/0001-use-async-sqlalchemy-and-mysql.md)。

## 2. 目录职责

```text
04_orm/
├── app/
│   ├── api/             # FastAPI 路由和 Depends 组装
│   ├── core/            # 配置、统一业务异常
│   ├── db/              # SQLAlchemy Base、Engine、Session
│   ├── models/          # 主表、子表 ORM 映射
│   ├── repositories/    # 查询、分页、关联数据访问
│   ├── schemas/         # 请求和响应 DTO
│   ├── services/        # 事务与业务用例
│   └── main.py          # ASGI 应用入口
├── docs/                # 领域模型与架构决策
├── examples/api.http    # 完整接口调用示例
├── sql/00_init.sql      # 建库、建表、种子数据
├── tests/               # 不依赖真实数据库的单元与 OpenAPI 测试
├── pytest.ini           # 子项目独立运行测试的配置
└── ruff.toml            # 继承仓库规则并声明本项目包边界
```

## 3. 准备环境

在仓库根目录执行：

```powershell
conda activate python-ai
python -m pip install -e ".[backend,dev]"
```

本项目已在本机 `.env` 中配置 `127.0.0.1:3306`、用户 `xiguapi` 和数据库 `customer_service_demo`。换电脑时不要复制真实密码，执行：

```powershell
Copy-Item src/fastapi2/04_orm/.env.example src/fastapi2/04_orm/.env
```

然后修改新生成的 `.env`。`.env` 已由仓库根目录 `.gitignore` 忽略，不能提交。

## 4. 初始化 MySQL

账号需要拥有 `customer_service_demo` 的建库/建表权限。进入项目目录后执行：

```powershell
Set-Location src/fastapi2/04_orm
mysql -h 127.0.0.1 -P 3306 -u xiguapi -p -e "source sql/00_init.sql"
```

命令会交互式询问密码，避免密码进入终端历史。SQL 可重复执行，种子数据不会重复插入。

生产环境不要给应用账号全局建库权限。应由 DBA/迁移账号执行 Alembic，应用账号只保留目标库的 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 权限。

## 5. 启动和访问

从 `04_orm` 目录运行：

```powershell
uvicorn app.main:app --reload
```

- Swagger UI：<http://127.0.0.1:8000/docs>
- 健康检查：<http://127.0.0.1:8000/health>
- 接口调用顺序：[examples/api.http](examples/api.http)

也可以从仓库根目录直接运行：

```powershell
uvicorn app.main:app --reload --app-dir src/fastapi2/04_orm
```

## 6. 主要接口

| 方法 | 路径 | 作用 |
|---|---|---|
| `POST` | `/api/v1/tickets` | 创建工单 |
| `GET` | `/api/v1/tickets` | 分页及条件查询 |
| `GET` | `/api/v1/tickets/{ticket_id}` | 工单与消息关联查询 |
| `PATCH` | `/api/v1/tickets/{ticket_id}` | 局部修改工单 |
| `DELETE` | `/api/v1/tickets/{ticket_id}` | 删除工单并级联消息 |
| `POST` | `/api/v1/tickets/{ticket_id}/messages` | 新增消息 |
| `GET` | `/api/v1/tickets/{ticket_id}/messages` | 分页查询消息 |
| `GET/PATCH/DELETE` | `/api/v1/tickets/{ticket_id}/messages/{message_id}` | 查询、修改、删除消息 |

## 7. 验证

在 `04_orm` 目录执行：

```powershell
ruff check app tests
ruff format --check app tests
mypy app
pytest -q
```

这些检查证明代码质量、类型和 OpenAPI 结构；只有 `/health` 返回 `database: up` 或执行真实 CRUD 后，才能说明数据库连接已验证。

## 8. 生产化下一步

当前项目刻意保持为可学习的简易 Demo。实际系统还应增加 Alembic 迁移、鉴权与数据权限、日志关联 ID、操作审计、幂等键、状态机、游标分页、指标监控、数据库 TLS 和密钥管理。
