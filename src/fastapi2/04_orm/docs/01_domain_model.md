# 客服工单领域模型
本文档记录编码前的领域边界和不变量，避免数据表只是随意拼凑的字段集合。

## 领域对象

```text
SupportTicket（工单，聚合根） 1 ────── N TicketMessage（消息，子实体）
```

- `SupportTicket` 是主表和聚合根，保存客户、主题、状态、优先级等工单级信息。
- `TicketMessage` 是子表，保存客户与客服在某一张工单中的沟通过程。
- 子表通过 `ticket_id` 外键归属主表，不允许消息脱离工单独立存在。

## 核心规则

1. 工单编号由服务端生成并建立唯一约束，客户端不能指定。
2. 工单状态只能是 `open`、`processing`、`resolved`、`closed`。
3. 优先级只能是 `low`、`medium`、`high`、`urgent`。
4. 消息发送方只能是 `customer`、`agent`、`system`。
5. 删除工单会级联删除消息；删除单条消息不会影响工单。
6. 更新和删除先用 `SELECT ... FOR UPDATE` 锁定目标行，避免并发写覆盖。

## 用例与接口

| 用例 | 方法与路径 | 数据访问特点 |
|---|---|---|
| 创建工单 | `POST /api/v1/tickets` | 单表写入，服务端生成编号 |
| 分页查工单 | `GET /api/v1/tickets` | `COUNT + LIMIT/OFFSET`，可过滤 |
| 工单关联详情 | `GET /api/v1/tickets/{id}` | `selectinload` 分批加载一对多消息 |
| 修改/删除工单 | `PATCH/DELETE /api/v1/tickets/{id}` | 事务内行锁；删除由外键级联 |
| 新增/分页查消息 | `POST/GET /api/v1/tickets/{id}/messages` | 先确认主表存在，再操作子表 |
| 查改删消息 | `GET/PATCH/DELETE /api/v1/tickets/{id}/messages/{message_id}` | 同时使用两个 ID，防止跨工单访问 |

## 刻意保留的简化

- 示例使用页码分页，便于学习；超大数据量或高频翻页应改为基于 `(created_at, id)` 的游标分页。
- 示例未加入登录鉴权、多租户、客服分配、状态流转权限和审计日志；这些属于真实客服系统的下一层能力。
- 邮箱这里只做长度校验。生产项目可增加 `email-validator`，并结合业务决定是否允许国际化邮箱。
