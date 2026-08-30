"""练习：JSON → JSON Schema → Pydantic → Structured Output 四层数据管道

场景：AI 简历信息提取（易速鲜花招聘「客服专员」）

运行（离线关卡可单独看；第 4 关需要 .env）：
  python 13_geektime_langchain/lessons/07b_data_pipeline_practice.py

练习建议：
  1. 先跑通全文，看四层输出
  2. 按文末 TODO 改代码，观察哪一层拦住脏数据
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import BaseModel, Field, ValidationError

# ---------------------------------------------------------------------------
# 共用：简历模型（第 3、4 关共用同一份蓝本）
# ---------------------------------------------------------------------------


class Resume(BaseModel):
    """一份「简历提取结果」的契约。"""

    name: str = Field(description="候选人姓名", min_length=1)
    experience_years: int = Field(description="工作年限（整数年）", ge=0, le=50)
    skills: list[str] = Field(description="技能列表", min_length=1)
    is_qualified: bool = Field(description="是否达到岗位最低要求（≥2 年经验）")


# =============================================================================
# 第 1 关：JSON —— 「写字的纸」（语法）
# =============================================================================


def gate1_json() -> None:
    print("\n=== 第 1 关：JSON（语法载体）===")

    # 合法 JSON 文本（跨语言都能传）
    text = '{"name": "小明", "experience_years": 3, "skills": ["客服", "沟通"], "is_qualified": true}'
    data = json.loads(text)
    print("解析成功：", data)
    print("类型：", type(data), "→ name 类型", type(data["name"]))

    # JSON 只管「能不能解析」，不管「语义对不对」
    bad_but_valid_json = '{"name": "小明", "experience_years": "三年", "skills": [], "is_qualified": true}'
    data2 = json.loads(bad_but_valid_json)
    print("语义很脏但 JSON 仍合法：", data2)
    print("  experience_years 实际类型：", type(data2["experience_years"]))  # str，不是 int


# =============================================================================
# 第 2 关：JSON Schema —— 「作文格子纸」（静态形状）
# =============================================================================


def gate2_json_schema() -> None:
    print("\n=== 第 2 关：JSON Schema（静态蓝图）===")

    # model_dump_json() 是「一份简历数据」；model_json_schema() 才是「格子纸」
    schema: dict[str, Any] = Resume.model_json_schema()
    print("Resume 的 JSON Schema（节选）：")
    print(json.dumps(
        {
            "title": schema.get("title"),
            "required": schema.get("required"),
            "properties": {
                k: {"type": v.get("type"), "description": v.get("description")}
                for k, v in schema.get("properties", {}).items()
            },
        },
        ensure_ascii=False,
        indent=2,
    ))
    print("说明：Schema 是说明书；它自己不会拦数据，需要校验器（第 3 关）去执行。")


# =============================================================================
# 第 3 关：Pydantic —— 「质检员 + 翻译官」（运行时校验）
# =============================================================================


def gate3_pydantic() -> None:
    print("\n=== 第 3 关：Pydantic（运行时校验 + 类型转换）===")

    # 通过：字符串 "3" 可转成 int
    ok = Resume.model_validate(
        {
            "name": "小明",
            "experience_years": "3",  # 文本 → int
            "skills": ["客服", "沟通"],
            "is_qualified": True,
        }
    )
    print("校验通过：", ok)
    print("  experience_years 类型：", type(ok.experience_years))

    # 拦截：年限为负数
    try:
        Resume.model_validate(
            {
                "name": "小红",
                "experience_years": -1,
                "skills": ["客服"],
                "is_qualified": False,
            }
        )
    except ValidationError as e:
        print("校验失败（年限 < 0）：", e.errors()[0]["msg"])

    # 拦截：skills 为空列表
    try:
        Resume.model_validate(
            {
                "name": "小刚",
                "experience_years": 5,
                "skills": [],
                "is_qualified": True,
            }
        )
    except ValidationError as e:
        print("校验失败（skills 为空）：", e.errors()[0]["msg"])


# =============================================================================
# 第 4 关：Structured Output —— 「命题作文」（约束模型生成）
# =============================================================================
#
# 说明：OpenAI 可用 llm.with_structured_output(Resume)（json_schema）。
# DeepSeek 等模型常报「This response_format type is unavailable now」，
# 改用「format_instructions + PydanticOutputParser」——契约仍是同一份 Resume。


def _resume_extract_chain(llm):
    """跨模型可用的结构化抽取：Schema 进 prompt → 模型出 JSON → Pydantic 校验。"""
    from langchain_core.output_parsers import PydanticOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    parser = PydanticOutputParser(pydantic_object=Resume)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是招聘助手。只输出合法 JSON，不要 markdown，不要解释。\n\n{format_instructions}",
            ),
            ("human", "{text}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    return prompt | llm | parser


def gate4_structured_output() -> None:
    print("\n=== 第 4 关：Structured Output（约束 LLM 输出形状）===")

    from langchain_openai import ChatOpenAI

    from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

    require_openai()

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        temperature=0,
    )

    chain = _resume_extract_chain(llm)

    raw_resume = """
    姓名：王芳
    做过 4 年电商客服，熟悉退换货与投诉处理，会用飞书和 Excel。
    """
    result = chain.invoke(
        {
            "text": (
                "从下面文本提取简历字段。"
                "岗位「客服专员」要求工作经验 ≥ 2 年，据此设置 is_qualified。\n\n"
                f"{raw_resume}"
            )
        }
    )
    print("模型结构化输出：", result)
    print("类型：", type(result))
    print("字段访问：", result.name, result.experience_years, result.is_qualified)


# =============================================================================
# 串联：四层一起用（简历提取小管道）
# =============================================================================


def pipeline_demo() -> None:
    print("\n=== 串联：Structured Output → Pydantic → JSON 落地 ===")

    from langchain_openai import ChatOpenAI

    from shared.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, require_openai

    require_openai()

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        temperature=0,
    )
    chain = _resume_extract_chain(llm)

    text = "李雷，1 年客服经验，会接待话术和工单系统。"
    obj = chain.invoke(
        {
            "text": "提取简历。岗位要求 ≥2 年经验，据此判断 is_qualified。\n" + text,
        }
    )

    # 「落地」：干净对象 → JSON 字符串（可写入 DB / 消息队列）
    stored = obj.model_dump_json(indent=2)
    print("入库 JSON：\n", stored)
    print("业务判断：", "通过初筛" if obj.is_qualified else "经验不足，人工复核")


# =============================================================================
# TODO 练习（自己改，观察哪一层拦住）
# =============================================================================
#
# TODO-1（第 1 关）：写一段非法 JSON（缺引号），用 try/except 捕获 json.JSONDecodeError

def gate1_json_practice() -> None:
    try:
        # json 格式错误，缺少引号
        json.loads('{"name": "小明", "experience_years": "三年", "skills": [], is_qualified: true}')
    except json.JSONDecodeError as e:
        print("JSON 解析失败：", e)

# TODO-2（第 3 关）：把 experience_years 的 le=50 改成 le=10，再喂 15 年经验，看谁报错

# 手写的 json schema 文件
RESUME_SCHEMA = {
    "type": "object",
    "required": ["name", "experience_years"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "experience_years": {"type": "integer", "minimum": 0, "maximum": 50},
    },
}

# 数据 data_info something


# TODO-3（第 4 关）：故意在 prompt 里要求「用中文写经验年数」，看 Structured Output
#         是否仍强制输出 int（对照：不用 structured，只用普通 invoke + StrOutputParser）
#
# TODO-4（串联）：把 is_qualified 的判定规则写进 Field(description=...)，看模型是否更稳


def main() -> None:
    # gate1_json()
    # gate1_json_practice()
    # gate2_json_schema()
    # gate3_pydantic()
    # 需要 API；若只想练 1～3 关，可注释下面两行
    # gate4_structured_output()
    pipeline_demo()
    # print("\n完成。请打开本文件底部 TODO 自己改一改。")


if __name__ == "__main__":
    main()
