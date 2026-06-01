"""
09 - 迷你 FastAPI（对应 daily-dev-tools 后端）

运行：
  pip install fastapi uvicorn
  uvicorn lesson:app --reload --port 8010

访问：
  http://127.0.0.1:8010/docs
  http://127.0.0.1:8010/hello/你的名字
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Python Learning Mini API")


class HelloResponse(BaseModel):
    message: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hello/{name}", response_model=HelloResponse)
def hello(name: str) -> HelloResponse:
    return HelloResponse(message=f"Hello, {name}")


# 对比典型 Web 项目结构：
# - main.py 创建 app
# - routes/ 定义路由
# - services/ 放业务逻辑
