-- 文件说明：一次性创建商品主库、最小权限账号、表结构和学习数据，便于新环境重复初始化。
-- 使用 MySQL 管理员账号执行；业务应用日常只使用 fastapi_app 账号。
-- 执行前将 CHANGE_ME_MYSQL_PASSWORD 替换为强密码，并同步写入 .env。

CREATE DATABASE IF NOT EXISTS fastapi_orm
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

CREATE USER IF NOT EXISTS 'fastapi_app'@'%'
    IDENTIFIED BY 'CHANGE_ME_MYSQL_PASSWORD';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON fastapi_orm.*
    TO 'fastapi_app'@'%';

FLUSH PRIVILEGES;

USE fastapi_orm;

CREATE TABLE IF NOT EXISTS products (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '商品ID',
    sku VARCHAR(64) NOT NULL COMMENT '业务唯一编码',
    name VARCHAR(120) NOT NULL COMMENT '商品名称',
    description TEXT NULL COMMENT '商品描述',
    price DECIMAL(12, 2) NOT NULL COMMENT '销售价格',
    stock INT NOT NULL DEFAULT 0 COMMENT '可用库存',
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uk_products_sku (sku),
    CONSTRAINT ck_products_price_positive CHECK (price > 0),
    CONSTRAINT ck_products_stock_non_negative CHECK (stock >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO products (sku, name, description, price, stock)
VALUES
    ('BOOK-PYTHON-001', 'Python 后端开发', 'FastAPI 与 SQLAlchemy 学习商品', 99.00, 100),
    ('BOOK-AI-001', '企业 AI 应用开发', 'RAG、Agent 与模型服务学习商品', 129.00, 50)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    description = VALUES(description),
    price = VALUES(price),
    stock = VALUES(stock);
