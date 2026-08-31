"""
05 - Agent 边界练习（无 API）

学完 14 章后，用纯 Python 把这几条边界写出来：
- Tool Call 是候选动作，不是已经执行
- 真正执行前先校验权限，拒绝时不能产生副作用
- Tool Result 必须带 tool_call_id
- Agent Loop 必须有确定性上限
- 模型输出：结构正确 ≠ 内容正确

运行：python 14_agent/05_practice.py
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------- 第 1 题：Tool Runtime 执行前校验 ----------
EXECUTED: list[str] = []


def refund_order(order_id: str) -> dict:
    EXECUTED.append(order_id)  # 真实副作用
    return {"refund_id": f"r_{order_id}"}


class ToolRuntime:
    def __init__(self) -> None:
        self.handlers = {"refund_order": refund_order}
        self.allowed_orders = {"ord_1001"}

    def execute(self, tool_call: dict) -> dict:
        # TODO：先判断权限；不允许时不要调用 handler。
        # 成功返回 {"tool_call_id": ..., "ok": True, "data": ...}
        # 失败返回 {"tool_call_id": ..., "ok": False, "error_code": "PERMISSION_DENIED"}
        raise NotImplementedError


runtime = ToolRuntime()
denied = runtime.execute(
    {"id": "call_1", "name": "refund_order", "arguments": {"order_id": "ord_9999"}}
)
assert denied["ok"] is False
assert denied["error_code"] == "PERMISSION_DENIED"
assert EXECUTED == [], "权限拒绝后不能执行 handler"

allowed = runtime.execute(
    {"id": "call_2", "name": "refund_order", "arguments": {"order_id": "ord_1001"}}
)
assert allowed["ok"] is True
assert EXECUTED == ["ord_1001"], "允许时才真实执行一次"
print("第 1 题通关 ✓：先校验，后执行")


# ---------- 第 2 题：Tool Result 必须带 tool_call_id ----------
def to_tool_result(tool_call: dict, data: dict) -> dict:
    # TODO：把 data 包装成 Tool Result，并保留 tool_call_id
    raise NotImplementedError


result = to_tool_result(
    {"id": "call_3", "name": "get_order", "arguments": {"order_id": "ord_1001"}},
    {"order_id": "ord_1001", "status": "shipped"},
)
assert result["tool_call_id"] == "call_3", "Tool Result 必须能关联回 Tool Call"
assert result["data"]["status"] == "shipped"
print("第 2 题通关 ✓：Tool Result 是下一轮输入，不是最终答案")


# ---------- 第 3 题：Agent Loop 必须有确定性上限 ----------
def get_weather(city: str) -> str:
    return f"{city} 18 度，阴天"


def run_agent_loop(fake_llm, messages: list, max_steps: int = 3) -> str:
    # fake_llm(messages) 返回 {"type": "tool_call", "tool": ..., "args": ...}
    # 或 {"type": "final", "text": ...}
    # TODO：循环最多 max_steps 次；达到上限还没 final 就返回 "stop_by_limit"
    raise NotImplementedError


class AlwaysTool:
    def __call__(self, messages: list) -> dict:
        return {"type": "tool_call", "tool": "get_weather", "args": {"city": "上海"}}


assert run_agent_loop(AlwaysTool(), [{"role": "user", "content": "天气"}]) == "stop_by_limit"
print("第 3 题通关 ✓：Loop 不能交给模型决定何时停止")


# ---------- 第 4 题：失败要有分类，不能盲目重试 ----------
@dataclass(frozen=True)
class ModelResult:
    ok: bool
    error_code: str | None = None


def is_retryable(result: ModelResult) -> bool:
    # TODO：timeout / rate_limited / overloaded 可重试；auth_error / refused 不可重试
    raise NotImplementedError


assert is_retryable(ModelResult(ok=False, error_code="timeout")) is True
assert is_retryable(ModelResult(ok=False, error_code="rate_limited")) is True
assert is_retryable(ModelResult(ok=False, error_code="overloaded")) is True
assert is_retryable(ModelResult(ok=False, error_code="auth_error")) is False
assert is_retryable(ModelResult(ok=False, error_code="refused")) is False
print("第 4 题通关 ✓：重试是有分类、有边界的恢复")


# ---------- 第 5 题：结构正确 ≠ 内容正确 ----------
ALLOWED_QUEUES = {"account", "payment", "technical"}
ALLOWED_PRIORITIES = {"low", "normal", "high"}


@dataclass(frozen=True)
class TicketRoute:
    queue: str
    priority: str
    reason: str


def validate_route(route: TicketRoute) -> str:
    # TODO：
    # 1) queue 不在允许范围 -> "INVALID_QUEUE"
    # 2) priority 不在允许范围 -> "INVALID_PRIORITY"
    # 3) priority 是 high 但 reason 太短（< 10 个字符）-> "INSUFFICIENT_REASON"
    # 4) 通过 -> "ok"
    raise NotImplementedError


assert validate_route(TicketRoute("finance", "normal", "合法长度原因")) == "INVALID_QUEUE"
assert validate_route(TicketRoute("account", "urgent", "合法长度原因")) == "INVALID_PRIORITY"
assert validate_route(TicketRoute("account", "high", "太短")) == "INSUFFICIENT_REASON"
assert validate_route(TicketRoute("account", "normal", "这个原因长度足够")) == "ok"
print("第 5 题通关 ✓：先结构校验，再业务规则校验")


print("\n5 道题全部通关 ✓")
