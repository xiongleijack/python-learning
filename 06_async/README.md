# 06 - 异步编程

Java 对照：这更像 **Netty / Vert.x 的事件循环**，不是 `ExecutorService` 开一堆线程。

| Java | Python |
| --- | --- |
| `@Async` / 新线程 | **不是** `async def`（调用不会开线程） |
| `EventLoop` 上挂 IO | `asyncio` 事件循环 + 协程 |
| `CompletableFuture.allOf` | `asyncio.gather` |
| `Future.get` 谁先好谁先取 | `asyncio.as_completed` |
| 阻塞调用丢线程池 | `asyncio.to_thread` |

`06_01_thread.py`、`06_02_asyncio.py` 是你的草稿，留着即可。

正式关卡（从上往下跑，assert 过了再进下一关）：

```bash
python 06_async/06_03_core.py
```
