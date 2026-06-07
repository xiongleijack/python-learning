from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.agents import create_tool_calling_agent, AgentExecutor
import os

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

# 定义工具
# 1. 定义工具
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
        "12345": "已发货，预计明天送达",
        "67890": "备货中，尚未发货",
    }
    return orders.get(order_id, f"订单 {order_id} 不存在")

tools = [get_weather, calculate, search_order]

# 2. 定义 prompt（agent_scratchpad 是 Agent 记录思考过程的地方）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手，尽可能使用工具回答用户问题，用中文回答。"),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # ← Agent 专用
])

llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=0)
agent = create_tool_calling_agent(llm, tools, prompt)

 # ← 打开 verbose=True 后能看到 Agent 每一步的思考过程
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "北京今天天气怎么样？"})
print(response["output"])

response = agent_executor.invoke({"input": "1 + 1 = ?"})
print(response["output"])

response = agent_executor.invoke({"input": "123456 订单信息怎么样？"})
print(response["output"])
