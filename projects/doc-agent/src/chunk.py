"""把长文档切成适合检索的小块。"""

from __future__ import annotations


def chunk_text(text: str, *, max_chars: int = 800, overlap: int = 100) -> list[str]:
    """
    TODO: 按字符数切块，相邻块 overlap 字符重叠。
    """
    raise NotImplementedError
