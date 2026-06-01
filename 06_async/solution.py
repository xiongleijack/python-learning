"""practice.py 参考答案"""

from __future__ import annotations

import asyncio


async def fetch_item(name: str, seconds: float) -> str:
    await asyncio.sleep(seconds)
    return name


async def fetch_all(names: list[str], seconds: float) -> list[str]:
    tasks = [fetch_item(name, seconds) for name in names]
    return list(await asyncio.gather(*tasks))
