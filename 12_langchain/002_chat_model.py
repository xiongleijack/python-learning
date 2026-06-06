"""
OpenAI Chat Completions API 示例（中转站配置见根目录 .env 的 OPENAI_*）
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
MAX_OUTPUT_TOKENS = int(os.environ.get("OPENAI_MAX_TOKENS", "1024"))

if not API_KEY:
    raise RuntimeError("请在 .env 配置 OPENAI_API_KEY")

log.info("API_BASE=%s", API_BASE)
log.info("MODEL=%s", MODEL)
log.info("API_KEY=%s...", API_KEY[:8])

client = OpenAI(api_key=API_KEY, base_url=API_BASE or None)

user_input = "请给我的花店想几个名字，不超过5个字"
log.info("请求 user=%r", user_input)

# chat.completions.create 常用参数：
#   model       模型 ID
#   messages    对话列表 [{"role": "system"|"user"|"assistant", "content": "..."}]
#   temperature 随机性 0~2
#   max_tokens  回复最长 token（部分 SDK 版本用 max_completion_tokens）
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a creative AI."},
        {"role": "user", "content": user_input},
    ],
    temperature=0.7,
    max_tokens=MAX_OUTPUT_TOKENS,
)


def format_chat_response(resp: ChatCompletion) -> str:
    """把 ChatCompletion 格式化成易读文本。"""
    choice = resp.choices[0]
    usage = resp.usage
    lines = [
        "=== Chat Completion ===",
        f"id:            {resp.id}",
        f"model:         {resp.model}",
        f"finish_reason: {choice.finish_reason}",
        f"prompt_tokens: {usage.prompt_tokens if usage else '-'}",
        f"completion:    {usage.completion_tokens if usage else '-'}",
        f"total_tokens:  {usage.total_tokens if usage else '-'}",
        "--- 回复 ---",
        choice.message.content or "",
    ]
    return "\n".join(lines)


def format_chat_response_json(resp: ChatCompletion) -> str:
    """JSON 格式化（调试用）。"""
    return json.dumps(resp.model_dump(), indent=2, ensure_ascii=False)


print(format_chat_response(response))

# 需要看完整结构时取消注释：
# print(format_chat_response_json(response))
