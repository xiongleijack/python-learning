"""LangGraph StateGraph Agent 示例（LangGraph 1.x 用 StateGraph，配置见 .env 的 OPENAI_*）"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

# 1. 定义工具
@tool
def get_weather(city: str) -> str:
    """根据城市名查询当前天气。"""
    data = {
        "北京": "晴天，25°C，微风",
        "上海": "多云，22°C，东风",
    }
    return data.get(city, f"暂无 {city} 的天气数据")

tools = [get_weather]
llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=0)
llm_with_tools = llm.bind_tools(tools)

# 2. 定义节点函数
def agent_node(state: MessagesState) -> MessagesState:
    """Agent 思考节点：调用模型"""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    """路由函数：有 tool_calls 走 tools，否则结束。"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 3. 构建图
graph = StateGraph(MessagesState)

# 添加节点
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))

# 添加边
graph.add_edge(START, "agent")            # 开始 → agent
graph.add_conditional_edges(              # agent → 根据条件分支
    "agent",
    should_continue,
    {"tools": "tools", END: END}
)
graph.add_edge("tools", "agent")          # 工具执行完 → 回到 agent

# 4. 编译
# 使用 MemorySaver 保存对话历史
checkpointer = MemorySaver()  
app = graph.compile(checkpointer=checkpointer)

# 5. 用 thread_id 区分不同会话
config = {"configurable": {"thread_id": "user_001"}}

# 第一轮
r1 = app.invoke(
    {"messages": [HumanMessage(content="我叫小明，北京天气怎么样？")]},
    config=config,
)
print("第一轮：", r1["messages"][-1].content)

# 第二轮（自动记住上轮内容）
r2 = app.invoke(
    {"messages": [HumanMessage(content="我叫什么名字？")]},
    config=config,
)
print("第二轮：", r2["messages"][-1].content)

# 不同 thread_id = 全新对话
config2 = {"configurable": {"thread_id": "user_002"}}
r3 = app.invoke(
    {"messages": [HumanMessage(content="我叫什么名字？")]},
    config=config2,
)
print("user_002：", r3["messages"][-1].content)  # 不知道名字

# 查看对话历史
print(app.get_state(config).values["messages"])
print(app.get_state(config2).values["messages"])