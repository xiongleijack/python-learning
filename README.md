# Python 学习框架（Java 程序员版）

独立仓库，按章节练习 Python。每章 `lesson.py` 讲解 + `practice.py` 动手。

## 环境

- Python 3.10+
- 终端进入本仓库根目录

```powershell
cd D:\my-code\github\python-learning
python --version
```

可选虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # 第 9～12 章需要
```

## 怎么用

1. 按 `00` → `12` 顺序学习（第 11 章 Excel、第 12 章 LangChain 可在 10 章后选做）。
2. 每章先跑 `lesson.py`，再完成 `practice.py`。
3. 一键跑某一章：

```powershell
.\run-lesson.ps1 -Lesson 06_async
```

4. 做完后在下方「进度」打勾。

### 在 Cursor / VS Code 里方便运行

1. **装扩展**：搜索并安装 [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)（微软官方）。
2. **选解释器**：`Ctrl+Shift+P` → `Python: Select Interpreter` → 选本仓库 `.venv`（先执行下面「环境」里的 `venv` 命令）。
3. **跑当前文件**（例如 `pass_test.py`）：
   - 编辑器右上角 **▶ Run Python File**；或
   - 打开终端后：`python 02_control_flow/pass_test.py`；或
   - `F5` 选 **Python: 当前文件**（可断点调试）。
4. **跑整章**：`Ctrl+Shift+P` → `Tasks: Run Task` → **Run Lesson: 选章节**。
5. **快捷键**：`Ctrl+Shift+B` 默认执行 **Python: 运行当前文件**（需先打开要运行的 `.py`）。

第 10 章读 `.env` 时，若路径不对，用 `F5` 选 **Python: 当前文件（仓库根目录）**。

## 进度

- [ ] 00 环境与运行
- [ ] 01 基础语法
- [ ] 02 控制流
- [ ] 03 集合与推导式
- [ ] 04 函数与模块
- [ ] 05 面向对象
- [ ] 06 异步编程
- [ ] 07 异常与文件
- [ ] 08 类型标注
- [ ] 09 实战：Mini API
- [ ] 10 Claude SDK API
- [ ] 11 Excel：按行拆分
- [ ] 12 LangChain 入门
- [ ] **实战** [智能体路线图](docs/agent-roadmap.md) → `projects/doc-agent`、`projects/sql-agent`

## 目录

```
python-learning/
├── 00_setup/
├── 01_basics/
├── 02_control_flow/
├── 03_collections/
├── 04_functions/
├── 05_oop/
├── 06_async/              # 新增：asyncio
├── 07_exceptions_io/
├── 08_typing/
├── 09_mini_api/
├── 10_claude_sdk/
├── 11_excel/              # Excel 按行拆分
├── 12_langchain/          # LangChain LCEL + RAG 入门
├── docs/
│   └── agent-roadmap.md   # 智能体实战计划
├── projects/
│   ├── doc-agent/         # 文档问答
│   └── sql-agent/         # SQL + Review 工作流
├── run-lesson.ps1
└── requirements.txt
```

## Java ↔ Python 速查

| Java | Python |
|------|--------|
| `public static void main` | `if __name__ == "__main__":` |
| `List<String>` | `list[str]` |
| `Map<K,V>` | `dict` |
| `record` / Lombok | `@dataclass` |
| `Maven/Gradle` | `pip` + `requirements.txt` |
| `CompletableFuture` / `@Async` | `async def` + `await`（第 6 章） |
| `Spring Boot` | FastAPI（第 9 章） |
| HTTP 客户端调 LLM | Anthropic SDK（第 10 章） |
| LLM 应用框架 | LangChain LCEL（第 12 章） |
| 花括号 `{}` | **缩进** |

## 学习节奏（建议 4～5 周）

| 周 | 章节 | 目标 |
|----|------|------|
| 1 | 00～03 | 语法、集合 |
| 2 | 04～05 | 函数、OOP |
| 3 | 06～08 | 异步、IO、类型 |
| 4 | 09 | 写一个小 API |
| 5 | 10 | Claude SDK |
| 选做 | 11 | Excel 办公自动化 |
| 选做 | 12 | LangChain（doc-agent 加速） |

## 第 12 章：LangChain 速查

| 概念 | 说明 |
|------|------|
| 安装 | `pip install langchain langchain-anthropic langchain-community` |
| LCEL | `chain = prompt \| llm \| StrOutputParser()` |
| 调用 | `chain.invoke({"topic": "..."})` |
| 文档 | `TextLoader` + `RecursiveCharacterTextSplitter` |
| RAG | `VectorStore` + `retriever` + LCEL |
| 运行 | `python 12_langchain/lesson.py` |

## 第 11 章：Excel 速查

| 概念 | 说明 |
|------|------|
| 安装 | `pip install openpyxl` |
| 读表 | `load_workbook(path, read_only=True)` |
| 写表 | `Workbook()` → `ws.append(row)` → `save()` |
| 运行 demo | `python 11_excel/lesson.py` |
| 练习 | 实现 `split_excel(source, output_dir, rows_per_file)` |

## 第 6 章：异步速查

| 概念 | 说明 |
|------|------|
| 协程 | `async def` 定义，调用需 `await` |
| 入口 | `asyncio.run(main())` |
| 并发等待 | `await asyncio.gather(...)` |
| 模拟 IO | `await asyncio.sleep(sec)` |
| 与 FastAPI | 路由里 `async def` 同理（第 9 章） |

## 第 10 章：Claude SDK 速查

| 概念 | 说明 |
|------|------|
| 安装 | `pip install anthropic python-dotenv` |
| 密钥 | 根目录 `.env`：`ANTHROPIC_API_KEY=...`（勿提交 Git） |
| 核心调用 | `client.messages.create(model=..., max_tokens=..., messages=[...])` |
| 系统提示 | `system="..."` 参数，不在 `messages` 里 |
| 多轮 | 把每轮 user/assistant 追加进 `messages` 列表 |
| 流式 | `client.messages.stream(...)` + `stream.text_stream` |

## 推送到 GitHub

```powershell
cd D:\my-code\github\python-learning
git init
git add .
git commit -m "chore: initial python learning framework"
git remote add origin https://github.com/你的用户名/python-learning.git
git branch -M main
git push -u origin main
```

## 资源

- [Python 官方教程](https://docs.python.org/3/tutorial/)
- [asyncio 文档](https://docs.python.org/3/library/asyncio.html)
- [FastAPI 教程](https://fastapi.tiangolo.com/zh/)
- [Anthropic Python SDK](https://platform.claude.com/docs/en/api/sdks/python)
- [Messages API 指南](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [智能体实战计划](docs/agent-roadmap.md)
- [列表推导式 vs 生成器表达式](docs/list-vs-generator.md)
- [LangChain 文档](https://python.langchain.com/docs/introduction/)
