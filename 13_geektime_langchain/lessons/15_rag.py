"""第 15 讲：检索增强生成 — RAG 助力鲜花运营

运行：python 13_geektime_langchain/lessons/15_rag.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, SAMPLE_DOCS, require_openai

require_openai()


def build_retriever():
    docs = []
    for path in SAMPLE_DOCS.glob("*.md"):
        docs.extend(TextLoader(str(path), encoding="utf-8").load())
    chunks = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=40).split_documents(docs)
    return FAISS.from_documents(chunks, FakeEmbeddings(size=128)).as_retriever(search_kwargs={"k": 2})


retriever = build_retriever()


@tool
def search_flower_docs(query: str) -> str:
    """检索易速鲜花运营文档（养护、配送、品类等）。"""
    docs = retriever.invoke(query)
    return "\n\n---\n\n".join(d.page_content for d in docs) or "未找到"


tools = [search_flower_docs]
llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, temperature=0)
llm_with_tools = llm.bind_tools(tools)


def agent_node(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def route(state: MessagesState):
    return "tools" if state["messages"][-1].tool_calls else END


graph = StateGraph(MessagesState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", route, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")
app = graph.compile()

result = app.invoke(
    {"messages": [HumanMessage(content="夏天玫瑰应该怎么存储？请查文档后回答。")]}
)
print(result["messages"][-1].content)
