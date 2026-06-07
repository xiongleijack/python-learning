from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=0.7)
parser = StrOutputParser()

# MessagesPlaceholder 是关键：历史消息会自动注入这里
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个编程助手，用中文回答。"),
    MessagesPlaceholder(variable_name="history"),  # ← 历史插入点
    ("human", "{input}"),
])

# 构建链 LLM + Prompt + Parser
chain = prompt | llm | parser

# 用字典存储每个用户的历史（key 是 session_id），实现多用户对话
store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 包装成有记忆的链
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 同一个 session_id = 同一段对话
config = {"configurable": {"session_id": "user_001"}}

r1 = chain_with_history.invoke({"input": "我叫小明"}, config=config)
print("第一轮：", r1)

r2 = chain_with_history.invoke({"input": "我叫什么名字？"}, config=config)
print("第二轮：", r2)

r3 = chain_with_history.invoke({"input": "我们聊了什么？"}, config=config)
print("第三轮：", r3)