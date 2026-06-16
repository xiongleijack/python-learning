"""极客时间 LangChain 实战课 — 章节入口

运行：python 13_geektime_langchain/lesson.py
单讲：python 13_geektime_langchain/lessons/01_setup.py
"""

from __future__ import annotations

from pathlib import Path

LESSONS = [
    ("01", "01_setup.py", "LangChain 系统安装和快速入门"),
    ("02", "02_knowledge_qa.py", "易速鲜花本地知识库问答"),
    ("03", "03_model_io.py", "模型 I/O"),
    ("04", "04_few_shot_prompt.py", "提示工程（上）FewShot"),
    ("05", "05_chain_of_thought.py", "提示工程（下）思维链"),
    ("06", "06_model_providers.py", "调用模型"),
    ("07", "07_output_parser.py", "输出解析"),
    ("08", "08_sequential_chain.py", "链（上）Sequential"),
    ("09", "09_router_chain.py", "链（下）Router"),
    ("10", "10_memory.py", "记忆 Memory"),
    ("11", "11_react_agent.py", "代理（上）ReAct"),
    ("12", "12_agent_executor.py", "代理（中）Agent"),
    ("13", "13_advanced_agents.py", "代理（下）高级 Agent"),
    ("14", "14_tools_toolkits.py", "Tool / Toolkits"),
    ("15", "15_rag.py", "RAG 检索增强"),
    ("16", "16_sql_database.py", "连接数据库"),
    ("17", "17_callbacks.py", "回调 Callbacks"),
    ("18", "18_camel.py", "CAMEL 角色扮演"),
    ("19", "19_baby_agi.py", "BabyAGI"),
    ("20", "20_network_tool_1.py", "人脉工具（上）"),
    ("21", "21_network_tool_2.py", "人脉工具（下）"),
    ("22", "22_chatbot_1.py", "客服机器人（上）"),
    ("23", "23_chatbot_2.py", "客服机器人（下）"),
]

LESSONS_DIR = Path(__file__).resolve().parent / "lessons"


def main() -> None:
    print("极客时间《LangChain 实战课》— 讲次列表\n")
    for num, filename, title in LESSONS:
        path = LESSONS_DIR / filename
        status = "OK" if path.exists() else "缺失"
        print(f"  第 {num} 讲  {title}")
        print(f"         python 13_geektime_langchain/lessons/{filename}  [{status}]")
    print("\n详见 README.md")


if __name__ == "__main__":
    main()
