"""
09 - Claude API（Anthropic Python SDK）

前置：完成 04（函数）、07（类型标注）会更顺手。

环境：
  pip install anthropic python-dotenv
  在仓库根目录创建 .env（已在 .gitignore）：
    ANTHROPIC_API_KEY=sk-ant-...

运行：
  python 09_claude_sdk/lesson.py

文档：
  https://platform.claude.com/docs/en/api/sdks/python
  https://platform.claude.com/docs/en/build-with-claude/working-with-messages

Java 对照：
  OkHttp / RestTemplate 发 HTTP    -> anthropic 封装 Messages API
  RequestBody + JSON               -> messages=[{"role": "user", "content": "..."}]
  流式 SSE                         -> client.messages.stream(...)
  环境变量 / Spring 配置           -> os.environ / .env
"""

from __future__ import annotations

import os
import sys
from typing import Any

# 默认模型：可按账号权限改成 claude-sonnet-4-6、claude-haiku-4-5 等
DEFAULT_MODEL = "claude-sonnet-4-6"


def load_api_key() -> str | None:
    """优先读环境变量；若安装了 python-dotenv 则加载仓库根目录 .env。"""
    try:
        from dotenv import load_dotenv

        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        load_dotenv(os.path.join(root, ".env"))
    except ImportError:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


def extract_text(message: Any) -> str:
    """从 messages.create 的响应里取出第一段文本。"""
    for block in message.content:
        if getattr(block, "type", None) == "text":
            return block.text
    return ""


def demo_message_shape() -> None:
    """不调用 API，只展示请求体结构（多轮对话靠追加 messages）。"""
    messages: list[dict[str, str]] = [
        {"role": "user", "content": "用一句话介绍 Python"},
        {"role": "assistant", "content": "Python 是一门强调可读性的通用语言。"},
        {"role": "user", "content": "和 Java 比呢？"},
    ]
    print("--- messages 列表示例 ---")
    for turn in messages:
        print(f"  {turn['role']:10} {turn['content'][:40]}...")


def demo_basic(client: Any) -> None:
    from anthropic import Anthropic

    assert isinstance(client, Anthropic)
    message = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": "用中文说：SDK 已连通"}],
    )
    print("--- 单次对话 ---")
    print(extract_text(message))
    print(f"  stop_reason={message.stop_reason}, usage={message.usage}")


def demo_system(client: Any) -> None:
    message = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=256,
        system="你是简洁的技术助教，回答用中文，不超过 80 字。",
        messages=[{"role": "user", "content": "什么是 max_tokens？"}],
    )
    print("--- system 参数 ---")
    print(extract_text(message))


def demo_stream(client: Any) -> None:
    print("--- 流式输出 ---")
    with client.messages.stream(
        model=DEFAULT_MODEL,
        max_tokens=128,
        messages=[{"role": "user", "content": "从 1 数到 5，每行一个数字"}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()


def main() -> None:
    demo_message_shape()

    api_key = load_api_key()
    if not api_key:
        print()
        print("未设置 ANTHROPIC_API_KEY，跳过在线演示。")
        print("在仓库根目录 .env 写入：ANTHROPIC_API_KEY=你的密钥")
        print("然后：pip install -r requirements.txt")
        return

    try:
        from anthropic import Anthropic
    except ImportError:
        print("请先安装：pip install anthropic python-dotenv", file=sys.stderr)
        sys.exit(1)

    client = Anthropic(api_key=api_key)
    demo_basic(client)
    demo_system(client)
    demo_stream(client)


if __name__ == "__main__":
    main()
