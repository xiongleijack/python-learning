import os
import time
from contextlib import contextmanager
from typing import Self


class Timer:
    def __enter__(self):
        self.start = time.time()
        print(f"start time..{self.start:.3f}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print(f"耗时 {self.end - self.start:.3f} 秒")
        return False


with Timer():
    total = sum(range(1_000_000))
    print(f"结果: {total}")


class DbConnection:

    name: str
    
    """
        构造方法函数
    """
    def __init__(self, name: str) -> None:
        """
        构造方法，DbConnection("mysql") 时会调用。
        self 相当于 Java 的 this；把传入的 name 存到对象上。
        """
        self.name = name

    def __enter__(self) -> Self:
        print(f"建立连接: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"关闭连接: {self.name}")
        # __exit__ 返回值决定是否“吞掉”异常：
        # True  = 抑制异常（异常被处理，不再向外抛）
        # False = 不抑制异常（异常继续向外传播）
        return False

with DbConnection(name="测试链接") as db:
    print(f"操作数据库{db.name}")

print("*" * 10 + " 更加简洁的写法 " + "*" * 10)


@contextmanager
def timer():
    start = time.time()
    print("开始计时")
    yield                       # ← with 块的代码在这里执行
    end = time.time()
    print(f"耗时 {end - start:.3f} 秒")

with timer():
    print("正在执行")

print("*" * 10 + " 简洁写法/写一个上下文管理器 cd(path)，进入时切换到指定目录，退出时切回原目录 " + "*" * 10)


@contextmanager
def pathChange(path: str):
    # 切换
    oldPath = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(oldPath)

with pathChange("/Users/leixiong/Documents/"):
    print("目录切换完成")


def add(a: int, b: int) -> int:
    return a + b

print(add("1", "2"))     # 会报错吗？



