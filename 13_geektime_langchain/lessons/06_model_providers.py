"""第 06 讲：调用模型 — OpenAI API / 开源模型

本仓库默认用 .env 的 OPENAI_*（中转站）。若课程演示 ChatGLM/Llama，在此单独实验。

运行：python 13_geektime_langchain/lessons/06_model_providers.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_openai import ChatOpenAI

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()

llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
print(llm.invoke("说一个适合情人节的易速鲜花热销品类").content)
