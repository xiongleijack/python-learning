"""将 SQL 写入文件并创建 Pull Request。"""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


def write_sql_file(sql: str, *, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    name = f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    path = out_dir / name
    path.write_text(sql.strip() + "\n", encoding="utf-8")
    return path


def create_pr(sql_path: Path, title: str, body: str) -> str:
    """
    TODO: git add / commit / gh pr create
    需配置 GITHUB_TOKEN、GITHUB_REPO
    """
    raise NotImplementedError("请实现 gh pr create 或 PyGithub")

    # 示例：
    # subprocess.run(["git", "add", str(sql_path)], check=True)
    # subprocess.run(["git", "commit", "-m", title], check=True)
    # subprocess.run(["gh", "pr", "create", "--title", title, "--body", body], check=True)
