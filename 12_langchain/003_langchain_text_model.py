"""LangChain ChatOpenAI 简单文本调用（配置见根目录 .env 的 OPENAI_*）

与 004 的区别：这里直接传字符串；004 用 SystemMessage / HumanMessage 结构化对话。

说明：langchain_openai.llms.OpenAI 走已逐渐淘汰的 /v1/completions 补全接口，
gpt-4.1-mini 等现代模型应使用 ChatOpenAI（/v1/chat/completions）。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=API_BASE,
    temperature=0.8,
    max_tokens=60,
)

response = llm.invoke("Please give me some names for my flower shop, no more than 5 words")
print(response.content)
