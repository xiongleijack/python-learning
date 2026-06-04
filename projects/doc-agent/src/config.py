"""读取 Anthropic 配置与文档根路径。"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_REPO_ROOT / ".env")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
DOC_ROOT = Path(os.environ.get("DOC_ROOT", _REPO_ROOT))
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
