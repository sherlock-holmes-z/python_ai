-- 文件说明：只负责创建审计库及最小权限账号，因为 PostgreSQL 建库不能依赖尚未创建的目标库连接。
-- 使用 psql 和 PostgreSQL 管理员账号执行；应用运行时不要使用管理员账号。
-- 本文件使用 psql 的 \gexec，因此不要放进普通事务中执行。
-- 执行前将 CHANGE_ME_POSTGRES_PASSWORD 替换为强密码，并同步写入 .env。

\set ON_ERROR_STOP on

SELECT 'CREATE ROLE fastapi_app LOGIN PASSWORD ''123456'''
WHERE NOT EXISTS (
    SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'fastapi_app'
) \gexec

ALTER ROLE fastapi_app PASSWORD 'CHANGE_ME_POSTGRES_PASSWORD';

SELECT 'CREATE DATABASE fastapi_orm OWNER fastapi_app ENCODING ''UTF8'''
WHERE NOT EXISTS (
    SELECT 1 FROM pg_database WHERE datname = 'fastapi_orm'
) \gexec
