# doc-agent — 项目文档问答

对 Markdown / 文本做索引，用 Claude 回答并引用来源。

## 结构

```
doc-agent/
├── src/
│   ├── config.py      # 读 .env、路径配置
│   ├── load_docs.py   # 扫描 md/txt
│   ├── chunk.py       # 切块
│   ├── index_store.py # Chroma 持久化
│   ├── ask.py         # Claude RAG 问答
│   ├── retrieve.py    # 检索 Top-K
│   └── cli.py         # 命令行入口
├── app/
│   └── streamlit_app.py
└── data/              # 向量库（本地，不提交 Git）
```

## 快速开始

```powershell
cd projects/doc-agent
pip install -r requirements.txt
copy .env.example .env   # 或共用仓库根 .env

python -m src.cli index --path D:\my-code\github\python-learning
python -m src.cli ask "asyncio.gather 和 as_completed 区别"

streamlit run app/streamlit_app.py
```

## 实现顺序

1. `load_docs` + `chunk` + 简单关键词 `retrieve`
2. `index_store`（Chroma）+ `ask`
3. Streamlit 页面
