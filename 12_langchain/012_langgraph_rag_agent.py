"""LangGraph + RAG Agent：从本地文档检索后回答（配置见 .env 的 OPENAI_*）

流程：加载 sample_docs → 切块 → FAISS 向量库 → search_docs 工具 → LangGraph Agent 循环
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

DOC_PATH = Path(__file__).resolve().parent / "sample_docs" / "06_async_notes.md"


def build_retriever():
    """加载本地 Markdown，切块并建 FAISS 索引（FakeEmbeddings 无需额外 Embedding Key）。"""
    docs = TextLoader(str(DOC_PATH), encoding="utf-8").load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30).split_documents(docs)
    vectorstore = FAISS.from_documents(chunks, FakeEmbeddings(size=128))
    return vectorstore.as_retriever(search_kwargs={"k": 2})


retriever = build_retriever()


@tool
def search_docs(query: str) -> str:
    """检索项目文档（async / LangChain 学习笔记），输入问题关键词，返回相关片段。"""
    docs = retriever.invoke(query)
    if not docs:
        return "文档未找到相关内容"
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


tools = [search_docs]
llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=0)
llm_with_tools = llm.bind_tools(tools)


def agent_node(state: MessagesState) -> MessagesState:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


graph = StateGraph(MessagesState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile()


def ask(question: str) -> str:
    result = app.invoke({"messages": [HumanMessage(content=question)]})
    return result["messages"][-1].content


print("--- RAG Agent 问答（基于 sample_docs/06_async_notes.md）---")
print(ask("gather 和 as_completed 的区别是什么？请根据文档回答。"))
print()
print(ask("什么时候应该用 gather？"))
