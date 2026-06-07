"""LangGraph StateGraph Agent 示例（LangGraph 1.x 用 StateGraph，配置见 .env 的 OPENAI_*）"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")


# 2. 定义节点函数
def agent_node(state: MessagesState):
    """Agent 思考节点：调用模型"""
    llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=0)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: MessagesState):
    """路由函数：决定下一步去哪"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"   # 有工具调用 → 去执行工具
    return END           # 没有 → 结束

# 3. 构建图
graph = StateGraph(MessagesState)

# 添加节点
graph.add_node("agent", agent_node)

# 添加边
graph.add_edge(START, "agent")            # 开始 → agent
graph.add_conditional_edges(              # agent → 根据条件分支
    "agent",
    should_continue,
    {"tools": "tools", END: END}
)

# 4. 编译
app = graph.compile()

# 5. 运行
result = app.invoke({
    "messages": [HumanMessage(content="北京天气怎么样？")]
})

print(result["messages"][-1].content)