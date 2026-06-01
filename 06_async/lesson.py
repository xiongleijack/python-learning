"""
06 - 异步编程（asyncio）

前置：04 函数、05 OOP；与 09 FastAPI 的路由 async def 一脉相承。

Java                          Python
Thread / Runnable             threading（本章不展开）
ExecutorService               asyncio + 协程
CompletableFuture             asyncio.Task / Future
@Async (Spring)               async def + await

运行：
  python 06_async/lesson.py
"""

from __future__ import annotations

import asyncio
import time


async def fetch_label(name: str, delay: float) -> str:
    """模拟 IO：等待时不阻塞整个进程，可切换去跑别的协程。"""
    await asyncio.sleep(delay)
    return f"{name} ok"


async def demo_await() -> None:
    print("--- await：顺序等待 ---")
    a = await fetch_label("A", 0.1)
    b = await fetch_label("B", 0.1)
    print(a, b)


async def demo_gather() -> None:
    print("--- gather：并发等待 ---")
    results = await asyncio.gather(
        fetch_label("X", 0.2),
        fetch_label("Y", 0.2),
        fetch_label("Z", 0.2),
    )
    print(results)


def sync_sequential() -> float:
    """同步写法：总耗时约 0.3s"""
    t0 = time.perf_counter()
    time.sleep(0.1)
    time.sleep(0.1)
    time.sleep(0.1)
    return time.perf_counter() - t0


async def async_concurrent() -> float:
    """异步写法：三次 sleep 并发，总耗时约 0.1s"""
    t0 = time.perf_counter()
    await asyncio.gather(
        asyncio.sleep(0.1),
        asyncio.sleep(0.1),
        asyncio.sleep(0.1),
    )
    return time.perf_counter() - t0


async def main() -> None:
    await demo_await()
    await demo_gather()

    sync_s = sync_sequential()
    async_s = await async_concurrent()
    print("--- 耗时对比（约）---")
    print(f"  同步顺序 sleep x3: {sync_s:.2f}s")
    print(f"  异步 gather sleep x3: {async_s:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
