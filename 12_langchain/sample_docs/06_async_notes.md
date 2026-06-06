# 06_async 章节摘要（供 LangChain RAG 演示）

## gather

`asyncio.gather` 并发执行多个协程，**全部完成后**按提交顺序返回结果列表。

## as_completed

`asyncio.as_completed` 也是并发，但**谁先完成谁先 yield**，适合实时打印进度。

## 对比

- gather：要完整结果、顺序固定 → 用 gather
- as_completed：先完先处理 → 用 as_completed
