"""第 12 讲：代理（中）— AgentExecutor 驱动模型与工具

课程用 AgentExecutor；LangChain 1.x 用 create_agent（见 12_langchain/009）。

运行：python 13_geektime_langchain/lessons/12_agent_executor.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()


@tool
def query_flower_price(flower: str) -> str:
    """查询花材参考单价（元/支）。"""
    prices = {"玫瑰": 8, "百合": 12, "康乃馨": 5, "向日葵": 6}
    price = prices.get(flower)
    if price is None:
        return f"暂无 {flower} 的报价"
    return f"{flower} 参考价 {price} 元/支"


llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, temperature=0)
agent = create_agent(
    model=llm,
    tools=[query_flower_price],
    system_prompt="你是易速鲜花店员，能查价时用工具，用中文回答。",
)

result = agent.invoke({"messages": [HumanMessage(content="玫瑰大概多少钱一支？")]})
last = result["messages"][-1]
print(last.content if isinstance(last, AIMessage) else last)
