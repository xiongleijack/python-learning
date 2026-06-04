# sql-agent — 规则内 SQL + Tool + Review

在业务规则约束下用 Claude 生成 SQL，经人工审批后可只读执行或创建 PR。

## 结构

```
sql-agent/
├── rules/
│   └── sql_rules.yaml    # 表白名单、禁止关键字
├── src/
│   ├── config.py
│   ├── validator.py      # SQL 硬规则校验
│   ├── tools.py          # list_tables、run_readonly_query 等
│   ├── agent.py          # Claude SDK tool loop
│   ├── git_ops.py        # 写 .sql 文件、gh pr create
│   ├── notify.py         # 钉钉/企微 webhook
│   └── cli.py
├── app/
│   └── streamlit_app.py  # Review 工作台
└── logs/                 # 审计日志
```

## 快速开始

```powershell
cd projects/sql-agent
pip install -r requirements.txt

python -m src.cli "查询最近 7 天 bond 表记录数"
python -m src.validator --sql "SELECT COUNT(*) FROM bond LIMIT 10"

streamlit run app/streamlit_app.py
```

## 安全

- 写操作（INSERT/UPDATE/DELETE）**只生成文件，不自动执行**
- 执行 SQL 前必须经 Streamlit / CLI 确认
- 数据库连接串仅放 `.env`

## 实现顺序

1. `validator.py` + `rules/sql_rules.yaml`
2. `tools.py`（mock 或只读库）
3. `agent.py` tool loop
4. `git_ops.py` + `notify.py`
5. Streamlit 审批页
