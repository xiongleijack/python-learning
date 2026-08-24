from ast import main
import logging
from math import log
import random
import re
from tkinter import E


logger = logging.getLogger(__name__)


def front_back(str):
    if len(str) <= 1:
        return str
    a = str[0]
    print(a)
    b = str[-1]
    print(b)
    c = str[1 : len(str) - 1]
    print(c)
    return a + b + c


def str_practice(str):
    print(str[0])
    print(str[1])
    print(str[-1])
    print(str[1:-1])


# 函数定义 -> 不声明类型
def sum1(a, b):
    return a + b


# 函数定义 -> 声明类型
def sum(a: int, b: int) -> int:
    return a + b


# 函数定义 -> 默认值
def sum2(a, b=2) -> int:
    return a + b


# 默认参数（类似Java重载）
def greet(name, greeting="Hello"):
    return greeting + " " + name


# 返回元组
def get_user():
    return "Alice", 25  # 返回元组，可以"返回多个值"


# 函数作用域, 声明要修改全局变量
a = 10


def change():
    # 声明修改全局变量
    global a
    a = 20
    print(a)


# 练习平方值
def squre(a):
    return a**2


# 创建数据字典
def create_prompt(system, user, temperature=0.7):
    return {"system": system, "user": user, "temperature": temperature}


# 返回元组
def parse_weather(weather, temperature):
    return weather, temperature


# 函数作为参数, 失败重试三次
def call_with_retry(func, retries=3):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            logger.warning("第 %s 次失败", i + 1, exc_info=False)
            if i == retries - 1:
                raise  # 异常抛出， 相当于java 里面的 throw exception


# 模拟一个可能失败的函数
def unstable_call():
    import random

    if random.random() < 0.5:
        raise Exception("随机失败")
    return "成功"


# 随机返回
def get_weather(city):
    return {
        "city": city,
        "temperature": random.randint(15,30),
        "condition": random.choice(["sunny", "cloudy", "rainy"]),
    }

# 模拟agent_tool 调用
def agent_call(tool_name, params):
    if tool_name == 'get_weather':
        return get_weather(params["city"])
    else:
        return {"error": f"未知工具：{tool_name}"}

if __name__ == "__main__":
    # front_back("abcd")
    # str_practice("xionglei")/
    # print(sum2(10))
    # print(get_user())
    # python 里面可以指定顺序，以下两行代码得到的结果是一样的
    # print(greet(greeting = "aaa", name = "bbb"))
    # print(greet("bbb", "aaa"))
    # change()
    # print(a)
    # call_with_retry(unstable_call)
    print(agent_call("get_weather", {"city": "上海"})["temperature"])
    print(agent_call("get_weather", {"city": "上海"})["condition"])

