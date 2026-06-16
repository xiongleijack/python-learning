"""第 08 讲：链（上）— SequentialChain 串联组件

课程用 SequentialChain；LangChain 1.x 推荐 LCEL（prompt | llm | parser）串联多步。
本示例：先生成标题，再扩写成推文。

运行：python 13_geektime_langchain/lessons/08_sequential_chain.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()

llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, temperature=0.7)
parser = StrOutputParser()

title_chain = ChatPromptTemplate.from_template("为易速鲜花 {product} 写一条 15 字以内标题") | llm | parser
body_chain = (
    ChatPromptTemplate.from_template("根据标题「{title}」写 50 字以内朋友圈推文")
    | llm
    | parser
)

full_chain = {"title": title_chain, "product": RunnablePassthrough()} | body_chain

print(full_chain.invoke("春季向日葵花束"))
