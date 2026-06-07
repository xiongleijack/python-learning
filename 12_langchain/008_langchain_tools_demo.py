from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

# 用 @tool 装饰器定义工具，docstring 很重要——模型靠它理解工具用途
@tool
def get_weather(city: str) -> str:
    """根据城市名查询当前天气，输入城市名称，返回天气信息，不要超过100个字。"""
    # 实际项目里这里调真实天气 API
    # 现在先 mock 数据
    weather_data = {
        "北京": "晴天，25°C，微风，空气质量优",
        "上海": "多云，22°C，东风，空气质量优",
        "广州": "小雨，28°C，南风，空气质量良",
    }
    return weather_data.get(city, f"暂无 {city} 的天气数据，请输入正确的城市名称。")

@tool
def calculate(expression: str) -> str:
    """计算数学表达式，输入合法的 Python 数学表达式，返回计算结果，不要超过100个字。"""
    try:
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算失败：{e}"

# 绑定工具到模型
llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=API_BASE, temperature=0)
llm_with_tools = llm.bind_tools([get_weather, calculate])

# 直接调用（还不是 Agent，模型只是决定要不要用工具）
response = llm_with_tools.invoke("北京今天天气怎么样？")
print(response.tool_calls)  # 看模型选了哪个工具，传了什么参数

response = llm_with_tools.invoke("1 + 1 = ?")
print(response.tool_calls)

response = llm_with_tools.invoke("上海今天天气怎么样？")
print(response.tool_calls)

response = llm_with_tools.invoke("广州今天天气怎么样？")
print(response.tool_calls)

response = llm_with_tools.invoke("北京今天天气怎么样？")
print(response.tool_calls)  