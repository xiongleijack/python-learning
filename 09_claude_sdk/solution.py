"""practice.py 参考答案（做完练习再对照）"""

from __future__ import annotations

from typing import Any, Literal

Role = Literal["user", "assistant"]


def build_messages(pairs: list[tuple[Role, str]]) -> list[dict[str, str]]:
    return [{"role": role, "content": content} for role, content in pairs]


def extract_text(message: Any) -> str:
    for block in message.content:
        if getattr(block, "type", None) == "text":
            return block.text
    return ""


def ask_claude(
    prompt: str,
    *,
    system: str | None = None,
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 256,
) -> str:
    from anthropic import Anthropic

    client = Anthropic()
    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system is not None:
        kwargs["system"] = system
    message = client.messages.create(**kwargs)
    return extract_text(message)
