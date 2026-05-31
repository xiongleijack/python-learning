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
pip install -r requirements.txt   # 第 8、9 章需要
```

## 怎么用

1. 按 `00` → `09` 顺序学习。
2. 每章先跑 `lesson.py`，再完成 `practice.py`。
3. 一键跑某一章：

```powershell
.\run-lesson.ps1 -Lesson 01_basics
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

第 9 章读 `.env` 时，若路径不对，用 `F5` 选 **Python: 当前文件（仓库根目录）**。

## 进度

- [ ] 00 环境与运行
- [ ] 01 基础语法
- [ ] 02 控制流
- [ ] 03 集合与推导式
- [ ] 04 函数与模块
- [ ] 05 面向对象
- [ ] 06 异常与文件
- [ ] 07 类型标注
- [ ] 08 实战：Mini API
- [ ] 09 Claude SDK API

## 目录

```
python-learning/
├── 00_setup/
├── 01_basics/
├── ...
├── 08_mini_api/
├── 09_claude_sdk/
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
| `Spring Boot` | FastAPI（第 8 章） |
| HTTP 客户端调 LLM | Anthropic SDK（第 9 章） |
| 花括号 `{}` | **缩进** |

## 学习节奏（建议 4 周）

| 周 | 章节 | 目标 |
|----|------|------|
| 1 | 00～03 | 语法、集合 |
| 2 | 04～05 | 函数、OOP |
| 3 | 06～07 | IO、类型 |
| 4 | 08～09 | Mini API + Claude SDK |

## 第 9 章：Claude SDK 速查

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
- [FastAPI 教程](https://fastapi.tiangolo.com/zh/)
- [Anthropic Python SDK](https://platform.claude.com/docs/en/api/sdks/python)
- [Messages API 指南](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
