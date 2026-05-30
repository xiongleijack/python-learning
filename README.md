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
pip install -r requirements.txt   # 第 8 章才需要
```

## 怎么用

1. 按 `00` → `08` 顺序学习。
2. 每章先跑 `lesson.py`，再完成 `practice.py`。
3. 一键跑某一章：

```powershell
.\run-lesson.ps1 -Lesson 01_basics
```

4. 做完后在下方「进度」打勾。

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

## 目录

```
python-learning/
├── 00_setup/
├── 01_basics/
├── ...
├── 08_mini_api/
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
| 花括号 `{}` | **缩进** |

## 学习节奏（建议 4 周）

| 周 | 章节 | 目标 |
|----|------|------|
| 1 | 00～03 | 语法、集合 |
| 2 | 04～05 | 函数、OOP |
| 3 | 06～07 | IO、类型 |
| 4 | 08 | 写一个小 API |

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
