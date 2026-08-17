import logging
from typing import Self

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


# 1. 自定义业务异常
class StudentDomainError(Exception):
    """学生业务异常基类。"""


class StudentNotFoundError(StudentDomainError):
    """学生不存在。"""


class ScoreOutOfRangeError(StudentDomainError):
    """成绩超出允许范围。"""


class DatabaseError(Exception):
    """模拟数据库异常。"""


# 2. 模拟数据库连接；with 会确保资源释放
class FakeDatabaseSession:
    def __enter__(self) -> Self:
        logger.info("打开数据库连接")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> bool:
        logger.info("关闭数据库连接")
        return False  # 不吞掉 with 代码块中的异常

    def student_exists(self, name: str) -> bool:
        return name in {"张三", "李四"}

    def save_score(self, name: str, score: int) -> None:
        if name == "数据库故障":
            raise DatabaseError("数据库暂时不可用")

        logger.info("保存成绩：%s = %s", name, score)


class StudentService:
    @staticmethod
    def parse_score(raw_score: object) -> int:
        """捕获多种输入异常，并保留原始异常链。"""
        try:
            return int(raw_score)  # type: ignore[arg-type]
        except (TypeError, ValueError) as exc:
            raise ValueError("成绩必须是整数") from exc

    @staticmethod
    def validate_score(score: int) -> None:
        """主动抛出业务异常。"""
        if not 0 <= score <= 100:
            raise ScoreOutOfRangeError("成绩必须在 0~100 之间")

    def record_score(self, name: str, raw_score: object) -> None:
        """录入成绩：演示 else、finally、异常透传。"""
        try:
            score = self.parse_score(raw_score)
            self.validate_score(score)

            # 推荐用 with 管理数据库连接、文件、锁等资源
            with FakeDatabaseSession() as session:
                if not session.student_exists(name):
                    raise StudentNotFoundError(f"学生不存在：{name}")

                session.save_score(name, score)

        except DatabaseError:
            # 记录上下文后，继续向上层抛出原异常
            logger.exception("保存成绩时发生数据库异常")
            raise

        else:
            # 只有整个 try 块没有异常时才执行
            logger.info("成绩录入成功：%s", name)

        finally:
            # 无论成功、失败、还是异常继续抛出，都会执行
            logger.info("本次录入流程结束：%s", name)


def main() -> None:
    service = StudentService()

    test_cases = [
        ("张三", "95"),  # 成功
        ("李四", "abc"),  # ValueError
        ("李四", 120),  # ScoreOutOfRangeError
        ("王五", 80),  # StudentNotFoundError
        ("数据库故障", 90),  # DatabaseError
    ]

    for name, raw_score in test_cases:
        print(f"\n--- 开始处理：{name}, {raw_score} ---")

        try:
            service.record_score(name, raw_score)

        except ValueError as exc:
            print(f"输入错误：{exc}")

        except StudentDomainError as exc:
            print(f"业务错误：{exc}")

        except DatabaseError as exc:
            print(f"系统错误，请稍后重试：{exc}")

        except Exception:
            # 最后一层兜底：记录完整堆栈，避免程序无日志退出
            logger.exception("未预期异常")

        finally:
            print("接口层收尾：记录请求日志、释放请求级资源")


if __name__ == "__main__":
    main()
