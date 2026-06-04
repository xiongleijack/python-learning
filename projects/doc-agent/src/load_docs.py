"""扫描目录下的 Markdown / 文本文件。"""

from __future__ import annotations

from pathlib import Path

DEFAULT_GLOBS = ("**/*.md", "**/*.txt")
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", "data"}


def load_documents(root: Path, globs: tuple[str, ...] = DEFAULT_GLOBS) -> list[dict[str, str]]:
    """
    TODO: 遍历 root，跳过 SKIP_DIRS，返回 [{"path": str, "content": str}, ...]
    """
    raise NotImplementedError
