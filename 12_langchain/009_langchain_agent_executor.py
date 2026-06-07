"""LangChain Agent 示例（LangChain 1.x 用 create_agent，配置见 .env 的 OPENAI_*）

与 008 的区别：008 只 bind_tools，模型决定调什么工具但不执行；
本文件用 create_agent 自动循环：选工具 → 执行 → 再喂给模型 → 直到给出最终答案。

旧版 AgentExecutor / create_tool_calling_agent 已移到 langchain-classic，此处用新 API。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")


@tool
def get_weather(city: str) -> str:
    """根据城市名查询当前天气。"""
    data = {
        "北京": "晴天，25°C，微风",
        "上海": "多云，22°C，东风",
        "广州": "小雨，28°C，南风",
    }
    return data.get(city, f"暂无 {city} 的天气数据")


@tool
def calculate(expression: str) -> str:
    """计算数学表达式，输入合法的 Python 表达式。"""
    try:
        return f"计算结果：{eval(expression)}"
    except Exception as e:
        return f"计算失败：{e}"


@tool
def search_order(order_id: str) -> str:
    """根据订单号查询订单状态。"""
    orders = {
        "123456": "已发货，预计明天送达",
        "67890": "备货中，尚未发货",
    }
    return orders.get(order_id, f"订单 {order_id} 不存在")


tools = [get_weather, calculate, search_order]

llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=0)

# debug=True 会在终端打印 Agent 每一步（类似旧版 verbose=True）
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个智能助手，尽可能使用工具回答用户问题，用中文回答。",
    debug=True,
)


def ask(question: str) -> str:
    """create_agent 返回 messages 列表，最后一条 AIMessage 即最终回答。"""
    result = agent.invoke({"messages": [HumanMessage(content=question)]})
    last = result["messages"][-1]
    if isinstance(last, AIMessage):
        return last.content
    return str(last)


# print(ask("北京天气怎么样？"))
# print(ask("1 + 1 = ?"))
# print(ask("123456 订单信息怎么样？"))
# 问一个没在工具列表中的问题，模型会怎么回答？
print(ask("刘若英的歌曲有哪些？"))
