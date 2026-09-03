# ADR-0001：使用异步 SQLAlchemy 2.x 连接 MySQL
- 状态：已采纳
- 日期：2026-09-04

## 背景

项目使用 FastAPI，并需要展示客服工单主子表的增删改查、分页和关联查询。本机可用数据库端口为 MySQL 默认端口 `3306`。

## 决策

1. 使用 SQLAlchemy 2.x ORM 和 `asyncmy`，通过 `AsyncSession` 执行非阻塞数据库访问。
2. API、Service、Repository、ORM Model、Pydantic Schema 分层。
3. Service 定义事务边界，Repository 只负责查询和数据变更，不自行 `commit()`。
4. 应用启动不调用 `create_all()`；建表由 `sql/00_init.sql` 显式完成，后续生产演进改用 Alembic。
5. 密码只写入被 Git 忽略的 `.env`，仓库中的 `.env.example` 使用占位符。

## 原因

- FastAPI 的并发模型适合搭配异步驱动，等待 MySQL 时不会阻塞事件循环线程。
- SQLAlchemy 是数据访问工具，不替代 Service 中的业务规则和事务编排。
- 显式迁移能审查、回滚并在不同环境重复执行；应用自动建表无法安全表达生产库结构演进。
- 主子表关系采用数据库外键和 ORM relationship 双重表达：前者保证数据完整性，后者方便关联查询。

## 影响

- 必须安装项目的 `backend` 可选依赖，并在启动前初始化数据库。
- 单进程内复用连接池；每个请求持有独立 Session，不能把 Session 缓存在全局变量中。
- 当前本地配置只适合学习。生产环境应使用密钥管理系统、最小权限账号和 TLS 连接。
