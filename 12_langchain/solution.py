"""practice.py 参考答案"""

from __future__ import annotations

import os

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def build_summary_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是简洁助教，用中文摘要，不超过 50 字。"),
            ("human", "解释：{topic}"),
        ]
    )
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    llm = ChatAnthropic(
        model=model,
        api_key=os.environ["ANTHROPIC_API_KEY"],
        max_tokens=256,
    )
    return prompt | llm | StrOutputParser()
