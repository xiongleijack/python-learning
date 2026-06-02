import asyncio
import time


async def agent_task(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} 完成"


def log(msg: str, t0: float) -> None:
    elapsed = time.perf_counter() - t0
    print(f"[{elapsed:5.2f}s] {msg}")


async def asyncio_gather() -> None:
    print("\n=== asyncio.gather（全部完成后，按提交顺序一次性返回）===")
    t0 = time.perf_counter()
    log("开始提交 3 个任务", t0)

    tasks = [
        agent_task("搜索", 3),
        agent_task("分析", 1),
        agent_task("写作", 2),
    ]
    results = await asyncio.gather(*tasks)

    for result in results:
        log(f"收到结果: {result}", t0)
    log("gather 结束", t0)


async def asyncio_as_completed() -> None:
    print("\n=== asyncio.as_completed（先完成的先收到）===")
    t0 = time.perf_counter()
    log("开始提交 3 个任务", t0)

    tasks = [
        agent_task("搜索", 3),
        agent_task("分析", 1),
        agent_task("写作", 2),
    ]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        log(f"收到结果: {result}", t0)
    log("as_completed 遍历结束", t0)


async def main() -> None:
    await asyncio_gather()
    await asyncio_as_completed()
    print("\n预期：gather 三条结果约在 3.00s 一起出现；as_completed 约在 1s / 2s / 3s 各出现一条。")


if __name__ == "__main__":
    asyncio.run(main())
