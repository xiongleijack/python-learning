"""配置：API Key、规则文件、数据库 URL。"""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_REPO_ROOT / ".env")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
NOTIFY_WEBHOOK_URL = os.environ.get("NOTIFY_WEBHOOK_URL", "")

RULES_PATH = Path(__file__).resolve().parents[1] / "rules" / "sql_rules.yaml"
LOGS_DIR = Path(__file__).resolve().parents[1] / "logs"


def load_rules() -> dict:
    with RULES_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)
