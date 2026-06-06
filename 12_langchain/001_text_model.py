"""
OpenAI Responses API  smoke test（中转站配置见根目录 .env 的 OPENAI_*）

常用参数见下方 responses.create(...) 注释。
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

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

user_input = "你能干啥？"
log.info("请求 input=%r", user_input)

# responses.create 常用参数：
#   model              模型 ID，需与中转站文档一致（如 gpt-4.1-mini）
#   input              用户输入，字符串或多轮 message 列表
#   instructions       系统指令（类似 system prompt），可选
#   temperature        0~2，越高越发散；0 更稳定
#   max_output_tokens  回复最长 token，控长度与费用
#   top_p              核采样，一般与 temperature 二选一，默认 1
#   store              是否保存 response，便于 previous_response_id 续聊
#   stream             True 则流式返回，需 for event in stream 处理
response = client.responses.create(
    model=MODEL,
    input=user_input,
    temperature=0.0,
    max_output_tokens=MAX_OUTPUT_TOKENS,
    store=True,
)
log.info("response.id=%s", getattr(response, "id", None))
log.info("response.status=%s", getattr(response, "status", None))
if getattr(response, "usage", None):
    log.info("usage=%s", response.usage)

print("--- 回复 ---")
print(response.output_text)
