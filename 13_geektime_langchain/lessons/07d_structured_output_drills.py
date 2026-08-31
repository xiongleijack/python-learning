"""
Structured Output：让 LLM 按 Pydantic 契约吐数据

Java                         Python
接口返回 DTO + Jackson        Pydantic 模型 + OutputParser
OpenAPI 约束响应体            format_instructions / with_structured_output

管道：自然语言 →（Schema 进 prompt）→ 模型出 JSON → Pydantic 校验 → 对象

DeepSeek 等模型往往用不了 llm.with_structured_output()。
本文件用「PydanticOutputParser + format_instructions」，契约仍是同一份模型。

怎么通关：先看示例跑通，再补 TODO。需要仓库根目录 .env 里的 OPENAI_API_KEY。
运行：
  python 13_geektime_langchain/lessons/07d_structured_output_drills.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0,
)

print("*" * 10 + " 示例：Schema 进 prompt，出来是模型不是 str " + "*" * 10)


class FlowerTip(BaseModel):
    flower: str = Field(description="花的名称")
    tip: str = Field(description="一句养护建议")


demo_parser = PydanticOutputParser(pydantic_object=FlowerTip)
print("塞进 prompt 的说明书（节选）：")
print(demo_parser.get_format_instructions()[:300], "...\n")

demo_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "只输出合法 JSON，不要 markdown，不要解释。\n\n{format_instructions}",
        ),
        ("human", "{text}"),
    ]
).partial(format_instructions=demo_parser.get_format_instructions())

demo_chain = demo_prompt | llm | demo_parser
demo = demo_chain.invoke({"text": "给玫瑰写一条浇水建议"})
print("类型：", type(demo))
print("点号访问：", demo.flower, "/", demo.tip)
print("-" * 10)

print("*" * 10 + " 练习：从文本抽出天气 " + "*" * 10)
# 定义 Weather
# - city: str
# - temperature: int   摄氏度整数
# - condition: str     如 sunny / cloudy / rainy
# 用 PydanticOutputParser + ChatPromptTemplate 拼 chain
# 输入：上海今天阴天，气温 18 度
# 通关：结果是 Weather，city 含「上海」，temperature 是 int


class Weather(BaseModel):
    # TODO：三个字段 + Field(description=...)
    city: str = "placeholder"


# TODO：parser / prompt / chain
weather = None
# TODO：invoke，把结果赋给 weather

assert weather is not None, "先把 chain 跑起来"
assert isinstance(weather, Weather), "应得到 Weather 对象，不是 str / dict"
assert "上海" in weather.city, "city 应从文本抽出上海"
assert isinstance(weather.temperature, int), "temperature 应是 int，不是「18 度」这种字符串"
print("Structured Output 关卡通关 ✓")
print(weather)
print("-" * 10)
print("记住：模型负责填空，Pydantic 负责验收。契约还是你写的那个 class。")
