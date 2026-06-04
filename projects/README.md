# 实战项目

学完 `06_async`、`10_claude_sdk` 后，在此目录动手做 Agent。

| 项目 | 说明 | 计划 |
|------|------|------|
| [doc-agent](./doc-agent/) | 文档问答、RAG | [agent-roadmap.md](../docs/agent-roadmap.md) 阶段 B |
| [sql-agent](./sql-agent/) | 规则内 SQL + Review + Tool | 阶段 C |

```powershell
# 文档 Agent CLI（实现 src 后）
cd projects/doc-agent
pip install -r requirements.txt
python -m src.cli index --path ../../
python -m src.cli ask "06 章 gather 是什么"

# SQL Agent CLI（实现 src 后）
cd projects/sql-agent
pip install -r requirements.txt
python -m src.cli "统计最近 7 天订单数"
```

密钥放在仓库根目录 `.env`（见各项目 `.env.example`）。
