"""第 03 讲：模型 I/O — 输入提示、调用模型、解析输出

运行：python 13_geektime_langchain/lessons/03_model_io.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()

# 1 输入提示
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是易速鲜花文案助手，输出简洁中文。"),
        ("human", "为{occasion}写一句 20 字以内的订花推荐语"),
    ]
)

# 2 调用模型
llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, temperature=0.8)

# 3 解析输出
# 3.1 文本输出
parser = StrOutputParser()
chain_text = prompt | llm | parser
result = chain_text.invoke({"occasion": "母亲节"})
print("文本输出：", result)

# 3.2 JSON 输出
parser = JsonOutputParser()
chain_json = prompt | llm | parser
result = chain_json.invoke({"occasion": "母亲节"})
print("JSON输出：", result)


