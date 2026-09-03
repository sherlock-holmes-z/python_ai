-- 本脚本由具备建库权限的 MySQL 账号执行；应用账号生产上应仅授予目标库所需权限。
CREATE DATABASE IF NOT EXISTS customer_service_demo
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;
USE customer_service_demo;

-- 主表保存工单当前状态和客户信息，业务明细不与消息正文混在同一行。
CREATE TABLE IF NOT EXISTS support_tickets (
    id BIGINT NOT NULL AUTO_INCREMENT,
    ticket_no VARCHAR(32) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(254) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_support_tickets PRIMARY KEY (id),
    CONSTRAINT uq_support_tickets_ticket_no UNIQUE (ticket_no),
    CONSTRAINT ck_support_tickets_status_values
        CHECK (status IN ('open', 'processing', 'resolved', 'closed')),
    CONSTRAINT ck_support_tickets_priority_values
        CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    INDEX ix_support_tickets_customer_email (customer_email),
    INDEX ix_support_tickets_status_created_at (status, created_at)
) ENGINE = InnoDB;

-- 子表保存沟通记录，外键级联保证删除工单后不会残留孤儿消息。
CREATE TABLE IF NOT EXISTS ticket_messages (
    id BIGINT NOT NULL AUTO_INCREMENT,
    ticket_id BIGINT NOT NULL,
    sender_type VARCHAR(20) NOT NULL,
    sender_name VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_ticket_messages PRIMARY KEY (id),
    CONSTRAINT ck_ticket_messages_sender_type_values
        CHECK (sender_type IN ('customer', 'agent', 'system')),
    CONSTRAINT fk_ticket_messages_ticket_id_support_tickets
        FOREIGN KEY (ticket_id) REFERENCES support_tickets (id) ON DELETE CASCADE,
    INDEX ix_ticket_messages_ticket_id_created_at (ticket_id, created_at)
) ENGINE = InnoDB;

-- 示例主数据使用固定 ticket_no，重复执行脚本不会重复插入。
INSERT INTO support_tickets (
    ticket_no,
    customer_name,
    customer_email,
    subject,
    status,
    priority
)
SELECT
    'CS-DEMO-0001',
    '张三',
    'zhangsan@example.com',
    '无法登录客服后台',
    'processing',
    'high'
WHERE NOT EXISTS (
    SELECT 1 FROM support_tickets WHERE ticket_no = 'CS-DEMO-0001'
);

-- 示例子数据同样用内容条件防重，便于学习时反复初始化。
INSERT INTO ticket_messages (ticket_id, sender_type, sender_name, content)
SELECT id, 'customer', '张三', '输入正确密码后仍提示登录失败。'
FROM support_tickets AS ticket
WHERE ticket.ticket_no = 'CS-DEMO-0001'
  AND NOT EXISTS (
      SELECT 1
      FROM ticket_messages AS message
      WHERE message.ticket_id = ticket.id
        AND message.content = '输入正确密码后仍提示登录失败。'
  );

INSERT INTO ticket_messages (ticket_id, sender_type, sender_name, content)
SELECT id, 'agent', '客服小李', '已收到问题，正在核对账号状态。'
FROM support_tickets AS ticket
WHERE ticket.ticket_no = 'CS-DEMO-0001'
  AND NOT EXISTS (
      SELECT 1
      FROM ticket_messages AS message
      WHERE message.ticket_id = ticket.id
        AND message.content = '已收到问题，正在核对账号状态。'
  );
