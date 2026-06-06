"""LangChain ChatOpenAI 多轮消息示例（配置见根目录 .env 的 OPENAI_*）"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

chat = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=API_BASE,
    temperature=0.8,
    max_tokens=60,
)

messages = [
    SystemMessage(content="You are a creative AI."),
    HumanMessage(content="Please give me some names for my flower shop, no more than 5 words"),
]

response = chat.invoke(messages)
print(response.content)
