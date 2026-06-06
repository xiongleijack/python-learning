# 第 12 章 LangChain 速读

> 前置：第 10 章 Claude SDK。建议先理解 Messages API，再用 LangChain 封装。

## LangChain 是什么

把 **Prompt、模型、解析器、文档加载、检索** 串成链（LCEL：`|` 管道），少写胶水代码。

| 第 10 章（原生 SDK） | 第 12 章（LangChain） |
|----------------------|------------------------|
| 自己拼 `messages` | `ChatPromptTemplate` |
| `client.messages.create` | `ChatAnthropic` |
| 手写 tool loop | `@tool` + `bind_tools`（进阶） |
| 自建 RAG | `DocumentLoader` + `VectorStore` + chain |

**建议**：MVP 用 SDK 搞懂原理；文档问答、多步链用 LangChain 提速。

## 安装

```powershell
pip install -r requirements.txt
```

> 说明：`langchain-community` 中部分集成在迁移到独立包，本章为学习方便仍使用 `TextLoader` / `FakeEmbeddings`；生产环境见 [LangChain 集成文档](https://python.langchain.com/docs/integrations/providers/) 选用官方包。

根目录 `.env`：

```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-6
```

## 本章文件

| 文件 | 内容 |
|------|------|
| `lesson.py` | LCEL 链、文档加载、简易 RAG |
| `practice.py` | 练习：实现摘要链 |
| `sample_docs/` | 本地示例 Markdown |
| `solution.py` | 参考答案 |

## 与实战项目的关系

| 本章 | 对应项目 |
|------|----------|
| DocumentLoader + split | `projects/doc-agent` |
| retriever + QA chain | `projects/doc-agent` |
| Tool / Agent（进阶） | `projects/sql-agent` → 复杂后可看 LangGraph |

## 资源

- [LangChain Python 文档](https://python.langchain.com/docs/introduction/)
- [ChatAnthropic](https://python.langchain.com/docs/integrations/chat/anthropic/)
