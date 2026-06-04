"""SQL 硬规则校验（在 LLM 输出之后、执行之前）。"""

from __future__ import annotations

import re

import sqlparse

from .config import load_rules


class SqlValidationError(ValueError):
    pass


def validate_sql(sql: str) -> None:
    """
    TODO: 检查 forbidden_keywords、allowed_tables、require_limit。
    通过则 return；不通过 raise SqlValidationError。
    """
    rules = load_rules()
    upper = sql.upper()

    for kw in rules.get("forbidden_keywords", []):
        if re.search(rf"\b{kw}\b", upper):
            raise SqlValidationError(f"禁止关键字: {kw}")

    if rules.get("require_limit") and "LIMIT" not in upper:
        raise SqlValidationError("SELECT 必须包含 LIMIT")

    # TODO: 解析表名并与 allowed_tables 比对
    _ = sqlparse.parse(sql)
    raise NotImplementedError("请完成表白名单校验")


if __name__ == "__main__":
    import sys

    sql = sys.argv[1] if len(sys.argv) > 1 else "SELECT 1"
    try:
        validate_sql(sql)
        print("校验通过")
    except (SqlValidationError, NotImplementedError) as e:
        print(f"校验失败: {e}")
