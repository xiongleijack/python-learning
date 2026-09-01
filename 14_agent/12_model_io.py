"""
1.2 从模型 API 到可控输入输出（无 API）

主链：
  可信上下文 → Adapter 组装请求 → 候选输出
  → Schema + 业务校验 → ModelResult → Loop 决定下一步

Loop 只消费 ModelResult，不解析堆栈、不绑死 Chat Completions / Responses。

运行：python 14_agent/12_model_io.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


print("*" * 10 + " 1. ModelResult：给 Loop 的稳定结构 " + "*" * 10)
# Java：统一 Result DTO，Controller 不 catch 一堆厂商异常


@dataclass
class ModelResult:
    ok: bool
    text: str | None
    error_code: str | None
    retryable: bool
    trace_id: str


def success(text: str, trace_id: str) -> ModelResult:
    # TODO：成功时应 ok=True，error_code=None，retryable=False
    raise NotImplementedError


def failure(error_code: str, retryable: bool, trace_id: str) -> ModelResult:
    # TODO：失败时应 ok=False，text=None
    raise NotImplementedError


ok_r = success("上海 18 度", "t-1")
assert ok_r.ok is True and ok_r.text == "上海 18 度" and ok_r.error_code is None
assert ok_r.retryable is False and ok_r.trace_id == "t-1"

bad_r = failure("TIMEOUT", True, "t-2")
assert bad_r.ok is False and bad_r.text is None
assert bad_r.retryable is True and bad_r.error_code == "TIMEOUT"
print("ModelResult 关卡通关 ✓")
print("-" * 10)


print("*" * 10 + " 2. 参数：能力配置，不是质量旋钮 " + "*" * 10)
# temperature：采样随机性（抽取/工具参数要低）
# top_p：核采样范围，通常与 temperature 二选一主调
# max_tokens：输出预算，太小会截断，别误判成格式错误


def validate_gen_config(temperature: float, top_p: float, max_tokens: int) -> None:
    # TODO：非法则 raise ValueError
    # temperature、top_p 落在 [0, 1]；max_tokens >= 1
    raise NotImplementedError


validate_gen_config(0.0, 1.0, 256)
caught = False
try:
    validate_gen_config(1.5, 0.9, 256)
except ValueError:
    caught = True
assert caught is True, "temperature 超范围应立刻终止，不要发给模型"
print("参数校验关卡通关 ✓")
print("-" * 10)


print("*" * 10 + " 3. 失败分类：不能 except Exception: retry() " + "*" * 10)
# auth / bad_param     → 立即终止
# timeout / network    → 有限重试 + 退避
# rate_limit           → 尊重 Retry-After，可退避
# schema               → 允许一次纠错重试
# refusal / truncate   → 不重试同请求；截断先加大预算


def classify(kind: str) -> tuple[str, bool]:
    """返回 (error_code, retryable)。"""
    # TODO
    raise NotImplementedError


assert classify("timeout") == ("TIMEOUT", True)
assert classify("rate_limit") == ("RATE_LIMIT", True)
assert classify("schema") == ("SCHEMA", True)
assert classify("auth") == ("AUTH", False)
assert classify("refusal") == ("REFUSAL", False)
print("失败分类关卡通关 ✓")
print("-" * 10)


print("*" * 10 + " 4. 结构正确 ≠ 内容正确 " + "*" * 10)
# 结构：字段/类型/枚举过了 Schema
# 内容：业务规则是否成立
# 模型不得自行生成 approved / 用户身份 / 主键


class Ticket(BaseModel):
    queue: Literal["finance", "support"]
    priority: Literal["low", "high"]
    amount: int = Field(ge=0)


def business_ok(ticket: Ticket) -> bool:
    # TODO：finance 队列的 amount 必须 >= 1000
    # support 的 high 也必须 >= 1000
    # 其它 True
    raise NotImplementedError


struct_ok = Ticket.model_validate({"queue": "finance", "priority": "high", "amount": 50})
assert struct_ok.queue == "finance"  # 枚举合法 → 结构正确
assert business_ok(struct_ok) is False  # 金额不够 → 内容不正确

struct_bad = False
try:
    Ticket.model_validate({"queue": "legal", "priority": "high", "amount": 50})
except ValidationError:
    struct_bad = True
assert struct_bad is True  # 枚举都过不了 → 结构就不正确

good = Ticket.model_validate({"queue": "finance", "priority": "high", "amount": 2000})
assert business_ok(good) is True
print("结构 vs 内容关卡通关 ✓")
print("-" * 10)


print("*" * 10 + " 5. 可信字段不能让模型填 " + "*" * 10)


class ModelDraft(BaseModel):
    summary: str
    queue: Literal["finance", "support"]


def attach_trusted(draft: ModelDraft, *, user_id: str, approved: bool) -> dict:
    # TODO：合并成对外结果。approved / user_id 只能来自参数，不能来自 draft
    raise NotImplementedError


draft = ModelDraft(summary="报销", queue="finance")
out = attach_trusted(draft, user_id="u-9", approved=False)
assert out["user_id"] == "u-9" and out["approved"] is False
assert out["queue"] == "finance"
print("可信字段关卡通关 ✓")
print("-" * 10)
print("1.2 代码关卡全部通关 ✓")
print("自测 4 题答完发给我验收，过了进 1.3 Streaming。")
