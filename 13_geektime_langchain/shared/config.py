"""极客时间课程共用配置：读取仓库根目录 .env"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
CHAPTER = Path(__file__).resolve().parents[1]
SAMPLE_DOCS = CHAPTER / "sample_docs"

load_dotenv(ROOT / ".env")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")


def require_openai() -> None:
    if not OPENAI_API_KEY:
        raise RuntimeError("请在仓库根目录 .env 配置 OPENAI_API_KEY")


def require_anthropic() -> None:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("请在仓库根目录 .env 配置 ANTHROPIC_API_KEY")
