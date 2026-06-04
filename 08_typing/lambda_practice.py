# 定义list
from ast import List
import re


bonds = [
    {"code": "240215.IB", "yield": 2.1},
    {"code": "123456.SH", "yield": 3.5},
    {"code": "240216.IB", "yield": 2.8},
]

# filter

# 生成器不产生列表，只保存一个状态机
squares_gen = (x*x for x in range(10**7))
total = sum(squares_gen)   # sum 函数会不断从生成器取一个值，累加，然后丢掉
print(total)    