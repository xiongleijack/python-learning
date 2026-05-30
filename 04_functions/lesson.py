"""
04 - 函数与模块

Java                    Python
method(a, b)            def func(a, b):
void                    -> None
可变参数 String...      *args
命名参数                **kwargs
static                  模块级函数（无 static 关键字）
"""


def add(a: int, b: int) -> int:
    return a + b


def log(message: str, *, level: str = "INFO") -> None:
    """* 后面是「仅关键字参数」，类似 Java 命名参数习惯"""
    print(f"[{level}] {message}")


def summarize(*values: int) -> tuple[int, float]:
    return sum(values), sum(values) / len(values)


def demo_import() -> None:
    # 同项目其他文件：from utils.helpers import format_name
    from pathlib import Path

    print(Path(__file__).name)


if __name__ == "__main__":
    print(add(2, 3))
    log("server started")
    log("error happened", level="ERROR")
    print(summarize(10, 20, 30))
    demo_import()
