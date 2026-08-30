"""
JSON → JSON Schema → Pydantic（四关）

Java                         Python
Jackson / Gson               json.loads / json.dumps
OpenAPI 文档                 JSON Schema（说明书，自己不跑）
@Valid + DTO                 pydantic.BaseModel

怎么通关：
- 每关先看示例，再补 TODO
- 从上往下跑本文件
- 打印「某关卡通关 ✓」= 过关
"""

from __future__ import annotations

import json
from typing_extensions import Required

from pydantic import BaseModel, Field, ValidationError

print("*" * 10 + " 第 1 关：JSON（写字的纸） " + "*" * 10)

# JSON 是文本。Python 里解析后通常是 dict / list。
demo = json.loads('{"name": "Ada", "age": 36}')
# print("示例解析：", demo, type(demo["age"]))  # age 是 int

# 脏数据也可以是「合法 JSON」——语法对就行，不管含义
dirty = json.loads('{"age": "三十六"}')
# print("语法合法但语义脏：", dirty, type(dirty["age"]))  # 这里是 str

# 练习 1
person = {"name": "Ada", "age": 36}
text = ""
text = json.dumps(person)
print(text)
# TODO：用 json.dumps 把 person 变成 JSON 字符串，赋给 text

back: dict = {}
# TODO：用 json.loads 把 text 解析回 dict，赋给 back
back = json.loads(text)

caught = False
# TODO：json.loads("{name: Ada}") 会失败。用 try/except json.JSONDecodeError，成功接到就 caught = True
try:
    json.loads("{name: Ada}")
except json.JSONDecodeError:
    caught = True

assert text.startswith("{") and '"name"' in text, "题 1：先 dumps"
assert back.get("name") == "Ada" and back.get("age") == 36, "题 1：再 loads 回来"
assert caught is True, "题 1：非法 JSON 要抓住 JSONDecodeError"
print("JSON 关卡通关 ✓")
print("-" * 10)

print("*" * 10 + " 第 2 关：JSON Schema（作文格子纸） " + "*" * 10)
# 总结：
# - JSON：特定格式的文本；和 Python dict 能互相转（dumps / loads）
# - JSON Schema：跨语言的说明书，不和任何一门语言绑定
#   里面写 string / integer，不是 Python 的 str / int，也不是 Java 的 String
#   自己不跑校验；Java 里对应 OpenAPI 文档，运行时靠 @Valid


# Schema 是说明书：类型 / 必填 / 最小值。它自己不会拦截脏数据。
# Java 不是没有：OpenAPI / Swagger 文档就是 JSON Schema；
# JDK 不自带，日常更常写成注解 @NotNull @Min，运行时靠 @Valid 执行。
# Python 里这份说明书经常单独是一份 dict/JSON，Pydantic 负责执行。
example_schema = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "age": {"type": "integer", "minimum": 0},
    },
}
print("示例 Schema 必填：", example_schema["required"])

# 练习 2：手写 Book 的 Schema（不要用 Pydantic 生成）
# 要求：
# - 整体是 object
# - 必填 title、price
# - title：字符串
# - price：number，最小值 0
BOOK_SCHEMA: dict = {}
# TODO：按上面要求填写 BOOK_SCHEMA
BOOK_SCHEMA = {
    "type": "object",
    "required": ["title", "price"],
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number", "minimum": 0}
    }
}


assert BOOK_SCHEMA.get("type") == "object", "题 2：type 应是 object"
assert set(BOOK_SCHEMA.get("required", [])) == {"title", "price"}, "题 2：必填 title、price"
props = BOOK_SCHEMA.get("properties", {})
assert props.get("title", {}).get("type") == "string", "题 2：title 是 string"
assert props.get("price", {}).get("type") == "number", "题 2：price 是 number"
assert props.get("price", {}).get("minimum") == 0, "题 2：price 最小 0"
print("JSON Schema 关卡通关 ✓")
print("记住：格子纸不会自己拦数据，下一关才是质检员。")
print("-" * 10)

print("*" * 10 + " 第 3 关：Pydantic（质检员 + 翻译官） " + "*" * 10)

class DemoUser(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=150)


print("从类导出的 Schema 标题：", DemoUser.model_json_schema().get("title"))
ok = DemoUser.model_validate({"name": "Bob", "age": "20"})  # "20" → 20
print("校验通过：", ok, type(ok.age))

# 练习 3：定义 Book，字段和上一关 Schema 对齐
# title: str，至少 1 个字符
# price: float，>= 0
class Book(BaseModel):
    # TODO：写字段，可用 Field(...)
    title: str = Field(min_length=1)
    price: float = Field(ge=0)

book = Book.model_validate({"title": "Python", "price": 39.9})
assert book.title == "Python" and book.price == 39.9, "题 3：合法数据应通过"

price_blocked = False
# TODO：用 try/except ValidationError 去校验 {"title": "x", "price": -1}
# 拦住负数价格后 price_blocked = True
try:
    Book.model_validate({"title": "x", "price": -1})
except ValidationError:
    price_blocked = True

assert price_blocked is True, "题 3：price < 0 应 ValidationError"
print("Pydantic 关卡通关 ✓")
print("-" * 10)

print("*" * 10 + " 第 4 关：嵌套模型 " + "*" * 10)
# Java：Address 是另一个 DTO，Person 里有 private Address address
# Pydantic：字段类型写成另一个 BaseModel，validate 时会递归校验


class Address(BaseModel):
    city: str
    street: str


class Person(BaseModel):
    name: str
    address: Address


nested = Person.model_validate(
    {"name": "Ada", "address": {"city": "上海", "street": "南京路"}}
)
print("嵌套访问：", nested.address.city, type(nested.address))

# 导出来的 Schema 里，address 也是 object（或 $ref 指向 Address）
addr_schema = Person.model_json_schema()
print("Person 的字段：", list(addr_schema.get("properties", {}).keys()))

# 练习 4：定义 Office
# - name: str
# - address: Address（复用上面的 Address，不要再写一遍 city/street）
# 通关：
#   Office.model_validate({"name": "HQ", "address": {"city": "北京", "street": "长安街"}})
#   得到 office.address.city == "北京"
#   缺少 street 时 ValidationError
class Office(BaseModel):
    # TODO
    name: str = "placeholder"


office_ok = None
# TODO：用嵌套 dict 构造 office_ok

assert office_ok is not None
assert office_ok.address.city == "北京", "题 4：应能点到嵌套字段 city"
assert isinstance(office_ok.address, Address), "题 4：address 应是 Address 对象，不是 dict"

nested_blocked = False
# TODO：校验 {"name": "HQ", "address": {"city": "北京"}}（缺 street），接到 ValidationError 则 nested_blocked = True

assert nested_blocked is True, "题 4：内层缺字段也要拦住"
print("嵌套模型关卡通关 ✓")
print("-" * 10)
print("四关全部通关 ✓  内层也是模型，不是普通 dict。")

# 序列化
book = Book(title="python", price=39.9)
print(book.model_dump())
print(book.model_dump_json())

# 反序列化
book = '{"title": "x", "price": 1}'
Book.model_validate_json(book)

class Item(BaseModel):
    name: str = Field(description="项目名称")
    age: int = Field(description="项目代码数据方式")

    def a(self):
        print(f"{self.name}, {self.age}")

item = Item(name= "text", age="3")
item.a()
print(type(item.age))
