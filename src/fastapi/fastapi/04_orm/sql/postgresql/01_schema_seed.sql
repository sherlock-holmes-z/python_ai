-- 文件说明：在审计库内创建日志表和示例记录，与管理员执行的建库步骤分离以降低权限范围。
-- 连接 fastapi_orm 数据库并使用 fastapi_app 账号执行。

CREATE TABLE IF NOT EXISTS product_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    action VARCHAR(32) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_product_audit_logs_product_id
    ON product_audit_logs (product_id);

CREATE INDEX IF NOT EXISTS ix_product_audit_logs_action
    ON product_audit_logs (action);

INSERT INTO product_audit_logs (product_id, action, payload)
SELECT
    1,
    'seeded',
    '{"source":"01_schema_seed.sql","message":"审计表初始化完成"}'::jsonb
WHERE NOT EXISTS (
    SELECT 1
    FROM product_audit_logs
    WHERE action = 'seeded'
      AND payload->>'source' = '01_schema_seed.sql'
);
