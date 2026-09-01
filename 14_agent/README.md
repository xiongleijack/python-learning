# 14 - Agent 学习

当前进度：**1.2 从模型 API 到可控输入输出**（1.1 已过关）

主链：

```
任务目标与可信上下文 → Model Adapter 组装请求
→ 模型返回候选输出 → Schema + 业务校验
→ 稳定 ModelResult 或错误语义 → Loop 决定下一步
```

Harness 装配的是 **Tools（工具 schema / 列表）**，不是 `tool_call`。`tool_call` 是模型之后产出的候选动作。

## 练习

| 文件 | 内容 | API |
| --- | --- | --- |
| `12_model_io.py` | ModelResult、参数校验、失败分类、结构 vs 内容 | 否 |

```bash
python 14_agent/12_model_io.py
```

过关后再进 **1.3 Streaming**。

自测题（可先写在脑子里或笔记里，再让我验收）：

1. 为什么「模型返回 JSON」不等于「业务已经正确」？
2. `temperature` / `top_p` / `max_tokens` 各管什么？为什么不是质量旋钮？
3. 超时、限流、Schema 失败，重试分别怎么做？
4. 什么是 `ModelResult`？为什么换模型不用改 Loop？
