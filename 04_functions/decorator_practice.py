"""
04 - 装饰器（Decorator）练习

Java 背景速记：
  Java 注解 @Override / @Autowired 是「元数据」，编译或框架读。
  Python @decorator 是「函数包函数」，运行时用 wrapper 替换原函数。

怎么练：
  1. 从上往下跑，看每关示例输出
  2. 补 TODO，assert 通过会打印「关卡通关 ✓」
  3. 和 LangChain 的 @tool 是同一套语法糖

运行：python 04_functions/decorator_practice.py
"""

from __future__ import annotations

import functools
import time
from typing import Callable, TypeVar
from unittest import result

F = TypeVar("F", bound=Callable)


# =============================================================================
# 第 0 关：装饰器本质 —— 函数接收函数、返回函数
# =============================================================================
print("=== 第 0 关：本质 ===")


def shout(func: Callable) -> Callable:
    """不用 @ 语法，手动包一层。"""

    def wrapper(*args, **kwargs):
        print("[before]")
        result = func(*args, **kwargs)
        print("[after]")
        return result

    return wrapper


def say_hello(name: str) -> str:
    return f"Hello, {name}"


# 手动装饰：say_hello = shout(say_hello)
# say_hello = shout(say_hello)
# say_hello("测试装饰器")


# =============================================================================
# 第 1 关：@ 语法糖
# =============================================================================
print("=== 第 1 关：@ 语法糖 ===")


def log_call(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}{args}{kwargs}")
        return func(*args, **kwargs)

    return wrapper


@log_call
def add(a: int, b: int) -> int:
    return a + b


# print(add(2, 3))
# print("-" * 10)

# 练习 1：写装饰器 uppercase_result，让函数返回值变成大写字符串
# 通关：@uppercase_result 装饰 greet 后，greet("java") == "HELLO, JAVA"
def uppercase_result(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"Hello, {str(result).upper()}"
    return wrapper

@uppercase_result
def output_str(str: str) -> str:
    return str

# print(output_str("python 你好"))

# =============================================================================
# 第 2 关：functools.wraps —— 保留原函数名字和文档
# =============================================================================
# print("=== 第 2 关：wraps ===")

def bad_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def good_decorator(func: Callable) -> Callable:
    # @functools.wraps(func)  # 把 __name__、__doc__ 复制回 wrapper
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@bad_decorator
def foo() -> None:
    """foo 的文档"""
    pass


@good_decorator
def bar() -> None:
    """bar 的文档"""
    pass


# print("bad:", foo.__name__, foo.__doc__)
# print("good:", bar.__name__, bar.__doc__)
# print("-" * 10)


# =============================================================================
# 第 3 关：带参数的装饰器（三层：decorator_factory → decorator → wrapper）
# =============================================================================
print("=== 第 3 关：带参数的装饰器 ===")


def repeat(times: int):
    """@repeat(3) 表示原函数执行 times 次（示例：只打印 side effect）。"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)

        return wrapper

    return decorator


@repeat(2)
def ping(msg: str) -> None:
    print(msg)


# ping("pong")
# print("-" * 10)

# 练习 2：实现 @prefix("【易速鲜花】")，把返回值前面加上前缀
# 通关：say_price("玫瑰") == "【易速鲜花】玫瑰 8 元/支"


def prefix(tag: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return tag + func(*args, **kwargs)
        return wrapper
    return decorator
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)  # 占位

        return wrapper

    return decorator


@prefix("【易速鲜花】")
def say_price(flower: str) -> str:
    return f"{flower} 8 元/支"


# print(say_price("玫瑰"))
# assert say_price("玫瑰") == "【易速鲜花】玫瑰 8 元/支", "练习 2 未通过"
# print("练习 2：改完 prefix 后取消 assert 注释")
# print("-" * 10)


# =============================================================================
# 第 4 关：实用装饰器 —— 计时
# =============================================================================
print("=== 第 4 关：计时装饰器 ===")


def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} 耗时 {elapsed:.4f}s")
        return result

    return wrapper


@timer
def slow_sum(n: int) -> int:
    return sum(range(n))


# print(slow_sum(1_000_000))
# print("-" * 10)

# 练习 3：写 cache_simple 装饰器，对无参函数缓存第一次结果（用闭包变量 dict）
# 通关：两次调用 expensive() 只 print 一次 "computing..."


def cache_simple(func: Callable[[], int]) -> Callable[[], int]:
    cached: dict[str, int] = {}

    @functools.wraps(func)
    def wrapper() -> int:
        if "value" in cached:
            return cached["value"]
        cached["value"] = func()
        return cached["value"]

    return wrapper


@cache_simple
def expensive() -> int:
    print("computing...")
    return 42


# print(expensive())
# print(expensive())
# print("-" * 10)


# =============================================================================
# 第 5 关：和 LangChain @tool 的关系
# =============================================================================
print("=== 第 5 关：和 @tool 的关系 ===")

# LangChain：
#
#   @tool
#   def get_weather(city: str) -> str:
#       '''查天气'''
#       ...
#
# @tool 也是装饰器：把普通函数变成 BaseTool，并读取 docstring 给模型看。
# 你已经在 12_langchain/008、009 里用过了，只是当时没展开语法。

# print("装饰器 = 在不改原函数代码的前提下，给函数「加一层行为」")
# print("-" * 10)


# =============================================================================
# 挑战（可选）
# =============================================================================
#
# TODO-A：写 @retry(max_attempts=3)，失败时重试，全失败再 raise
# TODO-B：写 @require_env("OPENAI_API_KEY")，没配置就 RuntimeError（可结合 dotenv）
#
# 参考 Java：装饰器 ≈ 手写 Wrapper / 动态代理里「前后加逻辑」，但写法更轻。


def main() -> None:
    print("\n完成基础示例。请做练习 1～3（取消 assert 注释并改 TODO）。")



if __name__ == "__main__":
    main()
