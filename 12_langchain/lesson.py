"""
12 - LangChain 入门（LCEL + 简易 RAG）

前置：10_claude_sdk（Messages API）、07_exceptions_io（Path）。

依赖：
  pip install langchain langchain-anthropic langchain-community langchain-text-splitters

运行：
  python 12_langchain/lesson.py

文档：
  https://python.langchain.com/docs/introduction/
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env")
    except ImportError:
        pass


def demo_lcel_summarize() -> None:
    """LCEL：prompt | llm | output_parser"""
    from langchain_anthropic import ChatAnthropic
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("--- LCEL 摘要链：跳过（未配置 ANTHROPIC_API_KEY）---")
        return

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是简洁助教，用中文回答，不超过 60 字。"),
            ("human", "用一句话解释：{topic}"),
        ]
    )
    llm = ChatAnthropic(model=model, api_key=api_key, max_tokens=256)
    chain = prompt | llm | StrOutputParser()

    print("--- LCEL 摘要链 ---")
    answer = chain.invoke({"topic": "Python 列表推导式"})
    print(answer)


def demo_load_and_split() -> list:
    """文档加载 + 切块（无需 API Key）"""
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    doc_path = Path(__file__).parent / "sample_docs" / "06_async_notes.md"
    loader = TextLoader(str(doc_path), encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
    chunks = splitter.split_documents(docs)

    print("--- 文档加载与切块 ---")
    print(f"  源文件: {doc_path.name}, 块数: {len(chunks)}")
    print(f"  首块预览: {chunks[0].page_content[:80]}...")
    return chunks


def demo_rag_qa(chunks: list) -> None:
    """InMemory 向量检索 + LCEL 问答（演示用 FakeEmbeddings，无需额外 Key）"""
    from langchain_anthropic import ChatAnthropic
    from langchain_community.embeddings import FakeEmbeddings
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.vectorstores import InMemoryVectorStore

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("--- 简易 RAG：跳过（未配置 ANTHROPIC_API_KEY）---")
        return

    embeddings = FakeEmbeddings(size=128)
    vectorstore = InMemoryVectorStore.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    def format_docs(docs) -> str:
        return "\n\n".join(d.page_content for d in docs)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "根据以下文档片段回答问题。若文档没有答案，请说「文档未提及」。\n\n{context}",
            ),
            ("human", "{question}"),
        ]
    )
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    llm = ChatAnthropic(model=model, api_key=api_key, max_tokens=512)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    question = "gather 和 as_completed 的区别是什么？"
    print("--- 简易 RAG 问答 ---")
    print(f"  问题: {question}")
    print(f"  回答: {chain.invoke(question)}")


def main() -> None:
    load_env()
    demo_lcel_summarize()
    chunks = demo_load_and_split()
    demo_rag_qa(chunks)


if __name__ == "__main__":
    main()
