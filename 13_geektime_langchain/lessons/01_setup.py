"""第 01 讲：LangChain 系统安装和快速入门

运行：python 13_geektime_langchain/lessons/01_setup.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0.7,
)

response = llm.invoke([HumanMessage(content="用一句话介绍易速鲜花是做什么的")])
print(response.content)
