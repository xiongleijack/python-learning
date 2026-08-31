# 14 - Agent 学习

> 前置：`07c` JSON / Schema / Pydantic，`07d` Structured Output。  
> Java 类比：Agent ≈ 一个会自己选方法调的服务；Tool ≈ `@RequestMapping` 的接口；循环 ≈ 直到不再 call 为止。

Agent 不是「再包一层 ChatGPT」，而是：

```
用户问题
  → 模型决定：直接回答，还是调用工具
  → 若调用：带 JSON 参数执行函数，把结果喂回模型
  → 再决定：继续调工具，还是给出最终回答
```

外层 `"type": "function"` 是工具种类；里面的 `parameters` 才是 JSON Schema。

## 目录

| 文件 | 内容 | 要 API？ |
| --- | --- | --- |
| `01_what_is_agent.py` | LLM vs Agent，mock 循环看一遍 | 否 |
| `02_tool_schema.py` | 手写 tool 描述（function + parameters） | 否 |
| `03_tool_loop.py` | 自己把「调工具 → 回填」写成循环 | 是（`.env`） |
| `04_structured_tool.py` | 工具入参用 Pydantic 校验 | 是 |
| `05_practice.py` | 5 道纯 Python 边界题：权限前置、tool_call_id、Loop 上限、失败分类、结构 vs 内容 | 否 |

## 怎么练

```bash
python 14_agent/01_what_is_agent.py
python 14_agent/02_tool_schema.py
# 根目录 .env 配好 OPENAI_API_KEY 后再跑 03、04
python 14_agent/03_tool_loop.py
# 无 API，随时可跑
python 14_agent/05_practice.py
```

后面实战：`projects/doc-agent`、`projects/sql-agent`（见 [agent-roadmap](../docs/agent-roadmap.md)）。LangChain 里的 ReAct 在 `13_geektime_langchain/lessons/11_react_agent.py`。
