"""Claude RAG 问答。"""

from __future__ import annotations

from anthropic import Anthropic

from .config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL


def build_rag_prompt(question: str, contexts: list[dict[str, str]]) -> str:
    blocks = []
    for i, ctx in enumerate(contexts, 1):
        blocks.append(f"[{i}] 来源: {ctx.get('source', '?')}\n{ctx.get('text', '')}")
    context_block = "\n\n".join(blocks) if blocks else "（无检索结果）"
    return f"""根据以下项目文档片段回答问题。若片段不足，请说明。
回答末尾用「来源:」列出引用编号。

文档片段：
{context_block}

问题：{question}
"""


def ask_claude(question: str, contexts: list[dict[str, str]]) -> str:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("请配置 ANTHROPIC_API_KEY")
    client = Anthropic()
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        system="你是项目文档助手，回答简洁，必须标注引用来源。",
        messages=[{"role": "user", "content": build_rag_prompt(question, contexts)}],
    )
    for block in message.content:
        if block.type == "text":
            return block.text
    return ""
