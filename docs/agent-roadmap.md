# 智能体实战路线图（SQL 工作流 + 文档问答）

> 技术选型：**Anthropic Python SDK（`anthropic`）**，MVP 手写 tool loop；工作流复杂后再引入 LangGraph。  
> 前置：完成本仓库 `06_async`、`10_claude_sdk`，建议了解 `09_mini_api`。

### 已确定：不用 claude-agent-sdk 作主栈

| 用 `anthropic` | 暂不用 Agent SDK 的原因 |
|----------------|-------------------------|
| SQL 规则校验 + 人工 Review 再执行 | Agent SDK 偏自主跑 Bash/Edit，审批链要额外约束 |
| doc-agent 向量 RAG | 自建 Chroma  pipeline 更可控、更省 token |
| 与第 10 章学习路径一致 | 先搞懂 Messages API + Tool Use |

以后若只做「自动生成 SQL 文件 + 开 PR」可单独开 POC；执行与校验仍走 `projects/sql-agent/`。

---

## 目标

| 项目 | 能力 | 成熟形态 |
|------|------|----------|
| **doc-agent** | 项目文档问答、整理 README/模块说明 | Streamlit 聊天页 + 索引按钮 |
| **sql-agent** | 规则内生成 SQL、Tool 调 API/只读库、Review 后提 PR/执行 | Streamlit 审批工作台 |

---

## 四阶段计划

### 阶段 A：基础（1～2 周）

**学习（本仓库）**

- [ ] `06_async` — 并发调 API、多任务
- [ ] `07_exceptions_io` — 配置、日志、容错
- [ ] `10_claude_sdk` — Messages API、system、流式

**产出**

- [ ] 能跑通 `10_claude_sdk/lesson.py`（配置 `.env` 中 `ANTHROPIC_API_KEY`）
- [ ] 读完 `projects/doc-agent/README.md` 与 `projects/sql-agent/README.md`

---

### 阶段 B：文档问答 MVP（2～3 周）— 优先

**目录：** `projects/doc-agent/`

| 周 | 任务 | 验收 |
|----|------|------|
| B1 | 实现 `load_docs` + `chunk_text` + 关键词检索 | CLI：`python -m src.cli ask "gather 和 as_completed 区别"` 能引用 `06_async` |
| B2 | 接入 Chroma 向量检索 + Claude 回答（带引用） | 回答末尾列出 `[来源: 文件路径]` |
| B3 | `app/streamlit_app.py` 聊天页 + 「重建索引」 | 浏览器内可问答 |

**暂不引入 LangChain**；理解索引 → 检索 → 生成的完整链路。

---

### 阶段 C：SQL Agent MVP（3～4 周）

**目录：** `projects/sql-agent/`

| 周 | 任务 | 验收 |
|----|------|------|
| C1 | `rules/sql_rules.yaml` + `validator.py` 禁写/表白名单 | `DELETE`、未授权表被拒绝 |
| C2 | `tools.py`：`list_tables`、`run_readonly_query`（mock 或只读库） | Tool 可被 agent 调用 |
| C3 | `agent.py` 手写 tool loop（Claude SDK） | 自然语言 → SQL 草稿 + 说明 |
| C4 | `git_ops.py` 生成 `.sql` 文件 + `gh pr create`；`notify.py` webhook | Review 前不自动执行写操作 |
| C5 | `app/streamlit_app.py`：展示 SQL → 按钮「批准只读执行」「创建 PR」 | 人工审批闭环 |

**安全原则**

- 默认只读账号；`INSERT/UPDATE/DELETE` 仅生成文件，不自动执行
- 所有执行记录写入 `logs/`
- 生产库连接串不进 Git，只用 `.env`

---

### 阶段 D：整合与可选升级（持续）

- [ ] 统一配置：两个项目共用 `.env` 模板
- [ ] SQL 工作流步骤 >5 且有分支时，评估 **LangGraph** 迁移 `sql-agent/src/agent.py`
- [ ] 文档 Agent：扫描 repo 自动生成/更新模块 README
- [ ] 部署：内网 FastAPI 或 Docker（可选）

---

## 项目目录

```
projects/
├── README.md
├── doc-agent/          # 文档问答
│   ├── src/
│   ├── app/
│   └── data/           # 本地索引（gitignore）
└── sql-agent/          # SQL 工作流
    ├── src/
    ├── app/
    ├── rules/
    └── logs/           # 审计（gitignore）
```

---

## 环境准备

```powershell
cd D:\my-code\github\python-learning
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 文档 Agent
pip install -r projects/doc-agent/requirements.txt

# SQL Agent
pip install -r projects/sql-agent/requirements.txt

# 根目录 .env（两个项目共用）
# ANTHROPIC_API_KEY=sk-ant-...
# ANTHROPIC_MODEL=claude-sonnet-4-6
```

---

## 里程碑检查表

| 日期（自填） | 里程碑 | 完成 |
|--------------|--------|------|
| | doc-agent CLI 能问答 | [ ] |
| | doc-agent Streamlit 上线 | [ ] |
| | sql-agent 规则校验通过 | [ ] |
| | sql-agent tool loop 跑通 | [ ] |
| | sql-agent Review + PR 流程 | [ ] |
| | 评估是否引入 LangGraph | [ ] |

---

## 资源

- [Anthropic Python SDK](https://platform.claude.com/docs/en/api/sdks/python)
- [Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Streamlit](https://docs.streamlit.io/)
- [Chroma](https://docs.trychroma.com/)
- 本仓库 `10_claude_sdk/`
