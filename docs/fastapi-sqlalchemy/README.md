# FastAPI 与 SQLAlchemy 学习笔记

> 根据原始 Word 文档的技术内容整理，已移除课程机构署名、品牌标题和宣传信息。

## 章节目录

- [协程](01-协程.md)：必学：理解异步调用、事件循环、Task、超时与取消
- [WSGI和ASGI](02-WSGI与ASGI.md)：必学：理解 FastAPI/Uvicorn 的异步服务运行边界
- [FastAPI](03-FastAPI.md)：重点：用于封装 LangChain/RAG/Agent 服务接口
- [SQLAlchemy](04-SQLAlchemy.md)：选学重点：用于对话、任务、反馈和业务数据持久化
- [FastAPI与SQLAlchemy结合案例（扩展）](05-FastAPI与SQLAlchemy综合案例.md)：实践：训练 API、依赖注入与数据库会话整合

## 推荐学习顺序

1. 先学习协程，理解 `async`、`await` 和事件循环。
2. 再学习 WSGI/ASGI，理解 Python Web 服务运行模型。
3. 学习 FastAPI 的路由、参数、请求体和模块拆分。
4. 按项目需要学习 SQLAlchemy ORM、Session、事务和关联关系。
5. 最后完成 FastAPI 与 SQLAlchemy 综合案例。

## LangChain 前置学习范围

如果目标是尽快进入 LangChain，优先完成前 3 章。SQLAlchemy 不是 LangChain 核心 API 的硬性前置，但在企业级 AI 服务中经常承担会话、任务、反馈和业务数据持久化，因此建议至少掌握 Engine、Session、事务、CRUD 和会话生命周期。
