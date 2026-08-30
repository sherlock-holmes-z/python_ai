<!-- 文件说明：统一领域术语和数据归属，避免代码、接口及数据库对同一概念产生不同理解。 -->

# 领域模型与术语

## Product（商品）

商品是本示例唯一可以通过 HTTP API 增删改查的聚合。MySQL 中的 `products` 表是其唯一事实来源。

| 字段 | 含义 | 约束 |
| --- | --- | --- |
| `id` | 数据库主键 | MySQL 自动生成 |
| `sku` | 业务唯一编码 | 只允许字母、数字、下划线和连字符 |
| `name` | 商品名称 | 1～120 个字符 |
| `description` | 商品描述 | 可以为空 |
| `price` | 商品价格 | 大于 0，最多两位小数 |
| `stock` | 可用库存 | 大于等于 0 |

## ProductAuditLog（商品审计日志）

记录商品写操作的结果快照，存储在 PostgreSQL。`product_id` 是跨数据库的逻辑引用，不能建立物理外键。

## Cache Aside

读取商品时先查询 Redis；未命中或缓存不可用时查询 MySQL，再回填 Redis。商品发生写操作后删除相应缓存，让下一次读取重新回源。

## Repository

只负责某一种数据库的 SQLAlchemy 查询和持久化，不包含 HTTP 状态码、缓存策略或跨存储编排。

## Service

编排 Repository、Redis 和审计写入，并抛出与 HTTP 框架无关的领域异常。
