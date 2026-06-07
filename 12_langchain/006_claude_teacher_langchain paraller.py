from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=1)

parser = StrOutputParser()

# 2. 定义三个组件，并行执行
summary_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是摘要助手，用一句话概括用户输入，不要超过10个字。"),
        ("human", "{input}"),
    ]) | llm | parser
)

keyword_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是关键词提取助手，提取3个关键词，用逗号分隔，不要超过10个字。"),
        ("human", "{input}"),
    ]) | llm | parser
)

# 情感倾向判断
sentiment_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是情感倾向判断助手，判断用户输入的情感倾向(正面、负面、中性)"),
        ("human", "{input}"),
    ]) | llm | parser
)

# 3. 用 | 串成一条链
chain = RunnableParallel({
    "summary": summary_chain,
    "keywords": keyword_chain,
    "sentiment": sentiment_chain,
})

# 4. 调用
result = chain.invoke({"input": "今天天气很好，心情很愉快"})
print(result["summary"])
print(result["keywords"])
print(result["sentiment"])