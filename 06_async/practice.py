"""
练习：用 asyncio 并发拉取「模拟数据」

1. fetch_item(name, seconds) — async，await asyncio.sleep(seconds) 后返回 name
2. fetch_all(names, seconds) — 用 asyncio.gather 并发，返回与 names 同序的列表

验证（有 asyncio，无需联网）：
  python 06_async/practice.py
"""

from __future__ import annotations

import asyncio


async def fetch_item(name: str, seconds: float) -> str:
    # TODO
    raise NotImplementedError


async def fetch_all(names: list[str], seconds: float) -> list[str]:
    # TODO: asyncio.gather
    raise NotImplementedError


async def _test() -> None:
    one = await fetch_item("git", 0.05)
    assert one == "git"

    result = await fetch_all(["a", "b", "c"], 0.05)
    assert result == ["a", "b", "c"]


if __name__ == "__main__":
    asyncio.run(_test())
    print("practice 06 通过 ✓")
