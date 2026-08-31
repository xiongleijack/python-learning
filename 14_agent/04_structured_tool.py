"""
04 - 工具入参用 Pydantic 校验

模型可能胡传参数。真正执行前用 model_validate，拦脏数据。
通关：parse_tool_args 能把合法 JSON 变成 WeatherArgs；缺 city 则 ValidationError。
"""

from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError


class WeatherArgs(BaseModel):
    city: str = Field(min_length=1, description="城市名")


def parse_tool_args(raw: str) -> WeatherArgs:
    # TODO：WeatherArgs.model_validate_json(raw)
    raise NotImplementedError


ok = parse_tool_args('{"city": "上海"}')
assert ok.city == "上海"

blocked = False
try:
    parse_tool_args("{}")
except (ValidationError, NotImplementedError):
    blocked = True
assert blocked is True, "缺 city 应拦住"
print("结构化工具入参关卡通关 ✓")
print("Agent 的 parameters Schema，执行前仍要 Pydantic 验一遍。")
