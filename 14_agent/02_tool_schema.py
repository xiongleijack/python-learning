"""
02 - 工具描述：type function vs JSON Schema

外层 type=function：告诉模型「这是一把可调用的工具」
内层 parameters：JSON Schema，描述入参长什么样

通关：补全 GET_WEATHER_TOOL，跑本文件通过 assert。
"""

from __future__ import annotations

# 示例：一个加法工具
ADD_TOOL = {
    "type": "function",
    "function": {
        "name": "add",
        "description": "两个整数相加",
        "parameters": {
            "type": "object",
            "required": ["a", "b"],
            "properties": {
                "a": {"type": "integer", "description": "加数"},
                "b": {"type": "integer", "description": "加数"},
            },
        },
    },
}
print("示例工具名：", ADD_TOOL["function"]["name"])
print("入参 Schema：", ADD_TOOL["function"]["parameters"]["required"])
print("-" * 10)

# 练习：写出 get_weather
# - type 为 function
# - 函数名 get_weather
# - 必填参数 city，类型 string
GET_WEATHER_TOOL: dict = {}
# TODO


fn = GET_WEATHER_TOOL.get("function", {})
params = fn.get("parameters", {})
assert GET_WEATHER_TOOL.get("type") == "function", "外层 type 应是 function，不是 object"
assert fn.get("name") == "get_weather"
assert params.get("type") == "object", "parameters 才是 JSON Schema，根类型是 object"
assert "city" in params.get("required", [])
assert params.get("properties", {}).get("city", {}).get("type") == "string"
print("工具 Schema 关卡通关 ✓")
print("type:function 是工具种类；type:object/string 才是 JSON Schema。")
