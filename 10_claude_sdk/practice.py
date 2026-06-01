"""
练习：Claude Messages API 常用封装

1. build_messages — 把 (role, content) 列表转成 API 需要的 dict 列表
2. extract_text — 从响应 content 块里取文本（lesson 里已有示例，这里自己实现一遍）
3. ask_claude — 可选：有 API Key 时发一次请求（见下方 __main__）

有 Key 时可在仓库根目录执行：
  python 10_claude_sdk/practice.py
"""

from __future__ import annotations

import os
from typing import Any, Literal

Role = Literal["user", "assistant"]


def build_messages(pairs: list[tuple[Role, str]]) -> list[dict[str, str]]:
    """TODO: 每个 pair 变成 {"role": ..., "content": ...}"""
    return []


def extract_text(message: Any) -> str:
    """TODO: 遍历 message.content，返回第一个 type=='text' 的 text"""
    return ""


def ask_claude(
    prompt: str,
    *,
    system: str | None = None,
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 256,
) -> str:
    """
    TODO: 使用 anthropic.Anthropic().messages.create 发请求并返回文本。
    system 为 None 时不传 system 参数。
    """
    raise NotImplementedError


if __name__ == "__main__":
    msgs = build_messages(
        [
            ("user", "你好"),
            ("assistant", "你好！"),
            ("user", "继续"),
        ]
    )
    assert len(msgs) == 3
    assert msgs[0] == {"role": "user", "content": "你好"}
    assert msgs[2]["role"] == "user"
    print("build_messages 通过 ✓")

    class _Block:
        def __init__(self, type_: str, text: str) -> None:
            self.type = type_
            self.text = text

    class _FakeMessage:
        content = [_Block("text", "ok"), _Block("text", "ignored")]

    assert extract_text(_FakeMessage()) == "ok"
    print("extract_text 通过 ✓")

    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            from dotenv import load_dotenv

            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            load_dotenv(os.path.join(root, ".env"))
        except ImportError:
            pass
        reply = ask_claude("回复一个字：好", system="只输出一个字")
        assert reply.strip()
        print(f"ask_claude 在线通过 ✓ 回复: {reply[:20]}...")
    else:
        print("未设置 ANTHROPIC_API_KEY，跳过 ask_claude 在线测试")
