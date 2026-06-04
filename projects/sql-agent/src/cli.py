"""sql-agent 命令行入口。"""

from __future__ import annotations

import argparse

from .agent import run_agent
from .notify import notify_review


def main() -> None:
    parser = argparse.ArgumentParser(description="SQL Agent CLI")
    parser.add_argument("request", nargs="?", default="查询 bond 表记录数")
    parser.add_argument("--notify", action="store_true", help="生成后发送 Review 通知")
    args = parser.parse_args()

    result = run_agent(args.request)
    print(result)

    if args.notify:
        notify_review("SQL Agent 待 Review", result[:500])


if __name__ == "__main__":
    main()
