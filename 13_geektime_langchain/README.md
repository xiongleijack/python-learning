# 第 13 章 极客时间《LangChain 实战课》

> 课程：黄佳 — [LangChain 实战课](https://time.geekbang.org/column/intro/100617601)（易速鲜花业务场景）  
> 前置：完成 `12_langchain/`；根目录 `.env` 配置 `OPENAI_*`（或课程中的 API Key）。

## 和 `12_langchain` 的关系

| 本章 | 第 12 章 |
|------|----------|
| 按**课程 23 讲**逐讲跟练 | 按**知识点**精简示例 |
| 易速鲜花场景 | 通用示例 |
| 部分讲次保留 **TODO**，对照课程 PDF/代码填写 | 已对齐 **LangChain 1.x** |

课程代码多基于 **LangChain 0.x**（`AgentExecutor`、`SequentialChain` 等）。本目录在注释中标明 **1.x 等价写法**；旧 API 需 `pip install langchain-classic`。

## 目录结构

```
13_geektime_langchain/
├── README.md
├── lesson.py              # 章节入口（列出全部讲次）
├── shared/config.py       # 读取根目录 .env
├── sample_docs/           # 易速鲜花本地知识库（演示用）
└── lessons/               # 01～23 讲，一讲一文件
    ├── 01_setup.py
    ├── 02_knowledge_qa.py
    └── ...
```

## 安装

依赖与第 12 章相同（仓库根目录）：

```powershell
pip install -r requirements.txt
```

## 怎么跑

**单讲：**

```powershell
python 13_geektime_langchain/lessons/01_setup.py
python 13_geektime_langchain/lessons/15_rag.py
```

**查看全部讲次：**

```powershell
python 13_geektime_langchain/lesson.py
```

## 课程目录对照

| 讲次 | 文件 | 模块 | 状态 |
|------|------|------|------|
| 01 | `01_setup.py` | 启程 | ✅ 可运行 |
| 02 | `02_knowledge_qa.py` | 启程 | ✅ 简易 RAG |
| 03 | `03_model_io.py` | 基础 | ✅ LCEL |
| 04 | `04_few_shot_prompt.py` | 基础 | TODO |
| 05 | `05_chain_of_thought.py` | 基础 | TODO |
| 06 | `06_model_providers.py` | 基础 | ✅ |
| 07 | `07_output_parser.py` | 基础 | ✅ |
| 08 | `08_sequential_chain.py` | 基础 | ✅ LCEL 串联 |
| 09 | `09_router_chain.py` | 基础 | TODO |
| 10 | `10_memory.py` | 基础 | TODO → 见 `12_langchain/007` |
| 11 | `11_react_agent.py` | 基础 | TODO → 见 `12_langchain/008` |
| 12 | `12_agent_executor.py` | 基础 | ✅ `create_agent` |
| 13 | `13_advanced_agents.py` | 基础 | TODO |
| 14 | `14_tools_toolkits.py` | 基础 | TODO |
| 15 | `15_rag.py` | 应用 | ✅ LangGraph + RAG |
| 16 | `16_sql_database.py` | 应用 | TODO |
| 17 | `17_callbacks.py` | 应用 | TODO |
| 18 | `18_camel.py` | 应用 | TODO |
| 19 | `19_baby_agi.py` | 应用 | TODO |
| 20 | `20_network_tool_1.py` | 实战 | TODO |
| 21 | `21_network_tool_2.py` | 实战 | TODO |
| 22 | `22_chatbot_1.py` | 实战 | TODO |
| 23 | `23_chatbot_2.py` | 实战 | TODO |

## 学习建议

1. 看一讲课 → 打开对应 `lessons/NN_*.py` → 把课程代码贴进 TODO 区（或新建 `notes/` 记笔记）。
2. 遇到 `AgentExecutor` / `SequentialChain` 报错 → 看文件头注释的 1.x 替代方案。
3. 第 15～23 讲与 `projects/doc-agent` 目标接近，可逐步迁到实战项目。

## 资源

- [LangChain 1.x 迁移指南](https://docs.langchain.com/oss/python/migrate/langchain-v1)
- 本仓库 `12_langchain/`、`docs/agent-roadmap.md`
