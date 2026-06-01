"""
08 - 类型标注（Java 程序员会觉得很亲切）

Java List<String>     list[str]
Java Map<String,Int>  dict[str, int]
Java Optional<T>      T | None
泛型擦除              运行时 list 不保留元素类型（typing 主要给 IDE/mypy）
"""

from typing import Callable


def find_first(items: list[str], predicate: Callable[[str], bool]) -> str | None:
    for item in items:
        if predicate(item):
            return item
    return None


def demo_union() -> None:
    value: str | int
    value = "ok"
    value = 200
    print(value)


if __name__ == "__main__":
    tools = ["git", "ai", "permission"]
    result = find_first(tools, lambda x: x.startswith("a"))
    print(result)
