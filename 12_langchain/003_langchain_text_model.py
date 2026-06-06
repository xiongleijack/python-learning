"""
LangChain + OpenAI 文本/对话模型示例（配置见根目录 .env 的 OPENAI_*）

LangChain 0.3+ 不再使用 langchain.llms，改为独立包 langchain_openai。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

# ChatOpenAI：走 /v1/chat/completions（gpt-4.1-mini 等对话模型）
# 若用 instruct 补全模型，改用：from langchain_openai import OpenAI
llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=API_BASE,
    temperature=0.8,
    max_tokens=60,
)

response = llm.invoke("请给我的花店起个名")
print(response.content)
