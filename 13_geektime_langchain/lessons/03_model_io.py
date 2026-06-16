"""第 03 讲：模型 I/O — 输入提示、调用模型、解析输出

运行：python 13_geektime_langchain/lessons/03_model_io.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是易速鲜花文案助手，输出简洁中文。"),
        ("human", "为{occasion}写一句 20 字以内的订花推荐语"),
    ]
)
llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, temperature=0.8)
parser = StrOutputParser()

chain = prompt | llm | parser
print(chain.invoke({"occasion": "母亲节"}))
