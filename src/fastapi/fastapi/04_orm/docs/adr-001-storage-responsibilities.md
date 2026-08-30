<!-- 文件说明：记录多数据源职责划分及其取舍，让后续维护者知道为什么采用当前架构。 -->

# ADR-001：MySQL、PostgreSQL 与 Redis 的职责划分

- 状态：已接受
- 日期：2026-08-29

## 背景

本项目用于学习 FastAPI、SQLAlchemy 2.x 异步 ORM、Redis 缓存，以及在一个服务中管理多个数据源。三个服务均部署在 `192.168.100.102`，连接凭据通过环境变量提供。

## 决策

- MySQL 是商品主数据的唯一事实来源，负责 `products` 表的增删改查。
- Redis 使用 Cache Aside 模式缓存单个商品详情，键格式为 `fastapi_orm:product:{id}`，默认 TTL 为 300 秒。
- PostgreSQL 保存商品创建、修改和删除的审计事件，不参与商品查询结果的生成。
- MySQL 和 PostgreSQL 使用不同的 SQLAlchemy `DeclarativeBase`、`AsyncEngine` 和 `AsyncSession`。
- Redis 客户端和数据库连接池在应用级复用，SQLAlchemy Session 按请求创建，不能跨并发任务共享。

## 一致性边界

教学版本先提交 MySQL 事务，再删除 Redis 缓存并尝试写 PostgreSQL 审计。Redis 或审计失败不会回滚已经提交的商品变更，因此这里只提供最终一致和降级能力，不提供跨库强一致。

生产环境如果要求审计事件不能丢失，应在 MySQL 同一事务中写入 Outbox 表，再由后台任务或消息队列投递到 PostgreSQL；不能使用当前的 best-effort 写入冒充分布式事务。

## 影响

### 优点

- 每种存储职责单一，适合观察 ORM、缓存和多数据源的边界。
- Redis 故障时商品查询可以回源 MySQL。
- PostgreSQL 审计故障不会阻断商品主业务。

### 代价

- 审计日志可能在 PostgreSQL 故障期间丢失。
- 缓存删除失败时，旧数据会一直保留到 TTL 到期。
- 两套关系数据库需要分别维护权限、连接池、迁移和监控。
