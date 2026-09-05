"""
06.03 协程核心（无网络）

Java 直觉要先拆掉：
  async def  ≠  @Async / new Thread
  调用 async 函数 → 只得到「尚未执行的协程对象」
  必须 await 或 asyncio.run，事件循环才会跑它

运行：python 06_async/06_03_core.py
"""

from __future__ import annotations

import asyncio
import inspect
import time

print("*" * 10 + " 1. 调用 async def 得到协程，不是返回值 " + "*" * 10)
# Java：普通方法一调用就开始跑；这里只是造了一个待调度的对象


async def ping() -> str:
    # TODO：返回 "pong"
    raise NotImplementedError


coro = ping()
assert inspect.iscoroutine(coro), "ping() 应得到 coroutine，立刻得到 str 说明写成了普通 def"
coro.close()  # 未 await 的协程要关掉，否则会 RuntimeWarning

assert asyncio.run(ping()) == "pong"
print("协程对象关卡通关 ✓")
print("-" * 10)


print("*" * 10 + " 2. await 之后才真正执行 " + "*" * 10)


async def double_later(n: int) -> int:
    # TODO：先等待约 0.01 秒（不阻塞事件循环），再返回 n * 2
    raise NotImplementedError


assert asyncio.run(double_later(4)) == 8
print("await 执行关卡通关 ✓")
print("-" * 10)


print("*" * 10 + " 3. 三个等待必须重叠，不能串成 0.15s " + "*" * 10)
# 事件循环单线程：time.sleep 会卡住所有协程
# 三个「等 0.05s」若重叠，总耗时应接近 0.05，而不是 0.15


async def nap(seconds: float) -> None:
    # TODO：等待 seconds 秒，且不能卡住整个事件循环
    raise NotImplementedError


async def three_naps() -> float:
    t0 = time.perf_counter()
    await asyncio.gather(nap(0.05), nap(0.05), nap(0.05))
    return time.perf_counter() - t0


elapsed = asyncio.run(three_naps())
assert elapsed < 0.12, "三个 nap 应重叠；若接近 0.15s，说明阻塞了事件循环"
print("并发等待关卡通关 ✓")
print("-" * 10)


print("*" * 10 + " 4. gather 按提交顺序返回 " + "*" * 10)
# 06_02 里你见过：gather 等齐后按入参顺序；as_completed 是谁先完谁先到


async def fetch_item(name: str, seconds: float) -> str:
    # TODO：等待 seconds 后返回 name
    raise NotImplementedError


async def fetch_all(names: list[str], seconds: float) -> list[str]:
    # TODO：并发拉取，返回顺序与 names 一致（慢的那个不能打乱顺序）
    raise NotImplementedError


async def _gate4() -> None:
    # 故意让中间那个更慢，顺序仍应是 a, b, c
    got = await asyncio.gather(
        fetch_item("a", 0.01),
        fetch_item("b", 0.04),
        fetch_item("c", 0.01),
    )
    assert got == ["a", "b", "c"]

    all_names = await fetch_all(["x", "y"], 0.01)
    assert all_names == ["x", "y"]


asyncio.run(_gate4())
print("gather 顺序关卡通关 ✓")
print("-" * 10)
print("06.03 全部通关 ✓  下一节：Task / create_task / 异常。")
