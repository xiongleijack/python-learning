"""
Claude SDK Tool Loop（手写 Agent，不用 LangGraph）。

流程：用户需求 → Claude → tool_use → 执行 tool → 继续对话 → 输出 SQL + 说明
"""

from __future__ import annotations

from anthropic import Anthropic

from .config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, load_rules
from .tools import TOOL_DEFINITIONS, dispatch_tool


def run_agent(user_request: str, *, max_turns: int = 10) -> str:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("请配置 ANTHROPIC_API_KEY")

    rules = load_rules()
    system = f"""你是 SQL 助手。只生成符合规则的 SELECT。
允许表: {rules.get('allowed_tables')}
禁止: {rules.get('forbidden_keywords')}
需要 LIMIT。先 list_tables 了解 schema，再生成 SQL。
最终给出 SQL 和简短说明。"""

    client = Anthropic()
    messages: list[dict] = [{"role": "user", "content": user_request}]

    for _ in range(max_turns):
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2048,
            system=system,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            texts = [b.text for b in response.content if b.type == "text"]
            return "\n".join(texts)

        if response.stop_reason != "tool_use":
            return f"意外 stop_reason: {response.stop_reason}"

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            try:
                output = dispatch_tool(block.name, block.input)
            except Exception as exc:
                output = f"Tool 错误: {exc}"
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                }
            )
        messages.append({"role": "user", "content": tool_results})

    return "超过最大轮数"


if __name__ == "__main__":
    import sys

    req = " ".join(sys.argv[1:]) or "查询 bond 表前 10 条"
    print(run_agent(req))
