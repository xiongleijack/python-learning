from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

# 2. 定义三个组件
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个英语老师"),
    ("human", "{input}"),
])

llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=1)

parser = StrOutputParser()

# 3. 用 | 串成一条链
chain = prompt | llm | parser

# 4. 调用
result = chain.invoke({"input": "帮我解释 serendipity 这个词"})
print(result)