"""定义可预期的业务异常，由 Web 层统一翻译为稳定的 JSON 错误响应。"""


class ApplicationError(Exception):
    """应用异常基类，不向客户端泄露数据库异常和堆栈细节。"""

    def __init__(self, *, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


class ResourceNotFoundError(ApplicationError):
    """查询目标资源不存在。"""

    def __init__(self, message: str) -> None:
        super().__init__(status_code=404, code="RESOURCE_NOT_FOUND", message=message)


class ResourceConflictError(ApplicationError):
    """唯一键等业务约束冲突。"""

    def __init__(self, message: str) -> None:
        super().__init__(status_code=409, code="RESOURCE_CONFLICT", message=message)


class InvalidOperationError(ApplicationError):
    """请求格式合法，但不满足当前业务操作要求。"""

    def __init__(self, message: str) -> None:
        super().__init__(status_code=422, code="INVALID_OPERATION", message=message)
