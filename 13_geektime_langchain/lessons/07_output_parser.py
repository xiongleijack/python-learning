"""第 07 讲：输出解析 — OutputParser 生成鲜花推荐列表

运行：python 13_geektime_langchain/lessons/07_output_parser.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()

parser = CommaSeparatedListOutputParser()
format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是鲜花顾问。{format_instructions}"),
        ("human", "预算 {budget} 元，推荐 3 种花材"),
    ]
).partial(format_instructions=format_instructions)

llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, temperature=0)
chain = prompt | llm | parser

flowers = chain.invoke({"budget": 200})
print("推荐列表：", flowers)
