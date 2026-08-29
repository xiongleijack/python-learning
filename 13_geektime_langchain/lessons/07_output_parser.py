"""第 07 讲：输出解析 — Str / List / Json / Pydantic

运行：python 13_geektime_langchain/lessons/07_output_parser.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.output_parsers import (
    CommaSeparatedListOutputParser,
    JsonOutputParser,
    PydanticOutputParser,
    StrOutputParser,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()

llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, temperature=0)

# 通用 prompt（Str / List 用）
base_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是易速鲜花助手，按用户要求输出。"),
        ("human", "{input}"),
    ]
)

# --- 3.1 文本 ---
chain_text = base_prompt | llm | StrOutputParser()
print("文本输出：", chain_text.invoke({"input": "用一句话介绍玫瑰"}))

# --- 3.2 列表 ---
list_parser = CommaSeparatedListOutputParser()
list_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "按格式输出。\n{format_instructions}"),
        ("human", "推荐 3 种适合母亲节的花材"),
    ]
).partial(format_instructions=list_parser.get_format_instructions())
chain_list = list_prompt | llm | list_parser
print("列表输出：", chain_list.invoke({}))

# --- 3.3 JSON 字典（标准写法：format_instructions + partial）---
class UserProfile(BaseModel):
    """JsonOutputParser 可挂 pydantic_object，生成 JSON schema 说明。"""

    name: str = Field(description="用户姓名")
    age: int = Field(description="用户年龄")


json_parser = JsonOutputParser(pydantic_object=UserProfile)
json_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是数据助手。只输出 JSON，不要代码、不要解释。\n\n{format_instructions}"),
        ("human", "{task}"),
    ]
).partial(format_instructions=json_parser.get_format_instructions())

chain_json = json_prompt | llm | json_parser
json_result = chain_json.invoke({"task": "根据描述生成用户信息：姓名张三，28 岁"})
print("JSON 输出：", json_result)
print("JSON 字段：", json_result["name"], json_result["age"])

# --- 3.4 Pydantic 对象（解析为模型实例，可 result.name 点号访问）---
class Permission(BaseModel):
    name: str = Field(description="权限编码，如 create_user")
    category: str = Field(description="权限分类，如 user")
    parent_code: str | None = Field(default=None, description="父权限编码，无则 null")


pydantic_parser = PydanticOutputParser(pydantic_object=Permission)
pydantic_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是权限配置助手。只输出 JSON，不要代码、不要解释。\n\n{format_instructions}"),
        (
            "human",
            "根据描述生成一条权限记录：\n"
            "功能：创建用户\n"
            "分类：user\n"
            "父权限：user_management",
        ),
    ]
).partial(format_instructions=pydantic_parser.get_format_instructions())

chain_pydantic = pydantic_prompt | llm | pydantic_parser
permission = chain_pydantic.invoke({})
print("Pydantic 输出：", permission)
print("Pydantic 字段：", permission.name, permission.category, permission.parent_code)
