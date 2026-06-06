"""LangChain ChatOpenAI 多轮消息调用（配置见根目录 .env 的 OPENAI_*）"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

# 1. 初始化模型
llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=API_BASE,
    temperature=0.7,
    max_tokens=1024,
)

# ── 方式一：直接传 messages（最基础） ──────────────────────────

# messages = [
#     SystemMessage(content="你是一个专业的 Python 编程助手，回答简洁清晰。"),
#     HumanMessage(content="什么是装饰器？"),
# ]

# response = llm.invoke(messages)
# print(response.content)

# # 手动维护多轮历史
# messages.append(AIMessage(content=response.content))
# messages.append(HumanMessage(content="能给我一个实际例子吗？"))

# response2 = llm.invoke(messages)
# print(response2.content)


# ── 方式二：ChatPromptTemplate（推荐生产使用） ─────────────────

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，用{language}回答问题。"),
    MessagesPlaceholder(variable_name="history"),  # 注入历史消息
    ("human", "{input}"),
])

chain = prompt | llm

# # 带变量调用
# result = chain.invoke({
#     "role": "数据分析专家",
#     "language": "中文",
#     "history": [],  # 第一轮没有历史
#     "input": "Pandas 和 Polars 哪个更快？",
# })
# print(result.content)


# ── 方式三：自动管理对话历史（多轮推荐） ──────────────────────

store = {}  # session_id -> ChatMessageHistory

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "user_001"}}

# 第一轮
r1 = chain_with_history.invoke(
    {"role": "编程助手", "language": "中文", "input": "什么是闭包？"},
    config=config,
)
print("第一轮:", r1.content)

# 第二轮（自动携带上轮历史）
r2 = chain_with_history.invoke(
    {"role": "编程助手", "language": "中文", "input": "能结合 Python 举例吗？"},
    config=config,
)
print("第二轮:", r2.content)


# ── 方式四：流式输出（Streaming） ─────────────────────────────

for chunk in chain_with_history.stream(
    {"role": "编程助手", "language": "中文", "input": "总结一下我们聊了什么"},
    config=config,
):
    print(chunk.content, end="", flush=True)
print()