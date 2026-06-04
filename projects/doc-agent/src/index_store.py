"""Chroma 向量索引的写入与查询。"""

from __future__ import annotations

from pathlib import Path


class DocIndex:
    """TODO: 封装 chromadb 持久化客户端。"""

    def __init__(self, persist_dir: Path) -> None:
        self.persist_dir = persist_dir

    def upsert(self, chunks: list[dict[str, str]]) -> None:
        """chunks: [{"id", "text", "source"}, ...]"""
        raise NotImplementedError

    def query(self, question: str, *, top_k: int = 5) -> list[dict[str, str]]:
        raise NotImplementedError
