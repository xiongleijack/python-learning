"""doc-agent 命令行：index / ask"""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import DATA_DIR, DOC_ROOT


def cmd_index(path: Path) -> None:
    print(f"TODO: 索引 {path} → {DATA_DIR}")
    # from .load_docs import load_documents
    # from .chunk import chunk_text
    # from .index_store import DocIndex


def cmd_ask(question: str) -> None:
    print(f"TODO: 检索并问答 — {question!r}")
    # from .index_store import DocIndex
    # from .retrieve import ask_claude


def main() -> None:
    parser = argparse.ArgumentParser(description="项目文档问答")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="重建文档索引")
    p_index.add_argument("--path", type=Path, default=DOC_ROOT)

    p_ask = sub.add_parser("ask", help="提问")
    p_ask.add_argument("question")

    args = parser.parse_args()
    if args.command == "index":
        cmd_index(args.path)
    elif args.command == "ask":
        cmd_ask(args.question)


if __name__ == "__main__":
    main()
