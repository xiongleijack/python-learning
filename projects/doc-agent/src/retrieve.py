"""从索引中检索与问题相关的文档块。"""

from __future__ import annotations


def keyword_search(question: str, chunks: list[dict[str, str]], *, top_k: int = 5) -> list[dict[str, str]]:
    """
    TODO: MVP 可用关键词匹配；后续改为 DocIndex.query。
    chunks: [{"text", "source"}, ...]
    """
    raise NotImplementedError
