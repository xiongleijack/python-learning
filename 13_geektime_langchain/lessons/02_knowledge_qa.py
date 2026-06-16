"""第 02 讲：基于「易速鲜花」本地知识库的智能问答（简易 RAG）

运行：python 13_geektime_langchain/lessons/02_knowledge_qa.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, SAMPLE_DOCS, require_openai

require_openai()


def load_vectorstore():
    docs = []
    for path in SAMPLE_DOCS.glob("*.md"):
        docs.extend(TextLoader(str(path), encoding="utf-8").load())
    chunks = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50).split_documents(docs)
    return FAISS.from_documents(chunks, FakeEmbeddings(size=128))


retriever = load_vectorstore().as_retriever(search_kwargs={"k": 2})

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是易速鲜花客服。仅根据以下资料回答，资料没有则说「文档未提及」。\n\n{context}"),
        ("human", "{question}"),
    ]
)
llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, temperature=0)
chain = (
    {
        "context": lambda q: "\n\n".join(d.page_content for d in retriever.invoke(q)),
        "question": lambda q: q,
    }
    | prompt
    | llm
    | StrOutputParser()
)

question = "易速鲜花同城配送多久能到？"
print(f"问：{question}")
print(f"答：{chain.invoke(question)}")
