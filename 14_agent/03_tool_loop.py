"""
03 - 手写 tool loop（需要 .env）

对照 01 的假模型：这里换成真 LLM。
循环：invoke → 若有 tool_calls 就执行函数 → 把结果追加进 messages → 再 invoke。

TODO：补全 run_agent。不要一开始就抄 LangChain AgentExecutor。
运行：python 14_agent/03_tool_loop.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "13_geektime_langchain"))

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

require_openai()


class WeatherArgs(BaseModel):
    city: str = Field(description="城市名")


def get_weather(city: str) -> str:
    return json.dumps({"city": city, "temperature": 18, "condition": "cloudy"}, ensure_ascii=False)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某城市天气",
            "parameters": WeatherArgs.model_json_schema(),
        },
    }
]

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0,
).bind_tools(TOOLS)


def run_agent(question: str) -> str:
    messages = [HumanMessage(content=question)]
    # TODO：最多循环 5 次
    # 1. ai = llm.invoke(messages)
    # 2. 若没有 tool_calls：return ai.content
    # 3. 否则对每个 tool_call：执行 get_weather，append ToolMessage
    #    ToolMessage(content=..., tool_call_id=tc["id"])
    return ""


if __name__ == "__main__":
    answer = run_agent("上海今天天气怎么样？")
    print("最终回答：", answer)
    assert answer, "run_agent 还没实现"
    print("tool loop 关卡通关 ✓")
