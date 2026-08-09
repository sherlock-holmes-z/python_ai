# WSGI和ASGI

WSGI和ASGI是Python Web开发中两个重要的接口规范，用于定义Web服务器与 Python Web应用之间的通信规则，二者的核心区别在于对异步的支持能力。

## 核心定位与目标

WSGI（Web Server Gateway Interface）是 Python 最早的 Web 服务器与应用接口规范（2003 年提出），仅支持同步操作，主要解决早期 Python Web 框架（如 Flask、Django 旧版本）与服务器的兼容性问题，让同一应用可以运行在不同的 WSGI 服务器上（如 Gunicorn、uWSGI）。

ASGI（Asynchronous Server Gateway Interface）是 WSGI 的异步升级版（2018 年提出），原生支持异步操作，同时兼容 WSGI。设计目标是解决 WSGI 无法高效处理异步任务（如 WebSocket、长轮询）的问题，为 FastAPI、Starlette 等异步框架提供标准接口。

## 工作流程差异

- WSGI 工作流程：
客户端发送请求 → WSGI 服务器接收 → 同步调用应用的 application(environ, start_response) 函数 → 应用处理后通过 start_response 返回响应 → 服务器转发响应。

整个过程是同步阻塞的，一个请求未处理完时，对应的线程 / 进程无法处理其他请求。

- ASGI 工作流程：
客户端发送请求 → ASGI 服务器接收 → 将请求封装为事件（如 http.request） → 通过事件循环异步传递给应用 → 应用处理后返回事件（如 http.response） → 服务器转发响应。

等待 I/O 操作（如数据库查询）时，事件循环会切换到其他请求，实现非阻塞处理。

## 如何选择

- 若使用同步框架（如 Flask、Django 3.0 之前版本），需用WSGI服务器（如 Gunicorn）。
- 若使用异步框架（如 FastAPI、Starlette、Django 3.1+ 异步模式），需用ASGI服务器（如Uvicorn）以发挥异步性能。
- 对于需要实时通信（如WebSocket聊天、实时数据推送）的场景，必须使用ASGI。
