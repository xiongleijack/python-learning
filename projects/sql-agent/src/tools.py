"""供 Claude 调用的 Tool 实现。"""

from __future__ import annotations

from .config import DATABASE_URL, load_rules
from .validator import SqlValidationError, validate_sql

TOOL_DEFINITIONS = [
    {
        "name": "list_tables",
        "description": "列出当前允许查询的表及 schema 说明",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "run_readonly_query",
        "description": "执行只读 SELECT（已通过规则校验）",
        "input_schema": {
            "type": "object",
            "properties": {"sql": {"type": "string", "description": "SELECT 语句"}},
            "required": ["sql"],
        },
    },
]


def list_tables() -> str:
    rules = load_rules()
    tables = rules.get("allowed_tables", [])
    hint = rules.get("schema_hint", "")
    return f"允许表: {', '.join(tables)}\n\n{hint}"


def run_readonly_query(sql: str) -> str:
    validate_sql(sql)
    if not DATABASE_URL:
        return f"[MOCK] 未配置 DATABASE_URL，SQL 已通过校验:\n{sql}"
    # TODO: 用 psycopg2/pymysql 连接只读库执行，带 timeout
    raise NotImplementedError("请接入只读数据库")


def dispatch_tool(name: str, inputs: dict) -> str:
    if name == "list_tables":
        return list_tables()
    if name == "run_readonly_query":
        return run_readonly_query(inputs.get("sql", ""))
    raise ValueError(f"未知 tool: {name}")
