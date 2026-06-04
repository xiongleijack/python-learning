"""
03 - 集合

Java              Python
List<T>           list
Map<K,V>          dict
Set<T>            set
stream().map()    列表推导式 [f(x) for x in items]
                  生成器表达式 (f(x) for x in items) 见 docs/list-vs-generator.md
Optional          常用 None + if 判断
"""

# Java: list.stream().filter(x -> x > 0).map(x -> x*2).collect(toList())
nums = [1, -2, 3, -4, 5]

# 写法 1：列表推导式（更 Pythonic）
result = [x * 2 for x in nums if x > 0]  # [2, 6, 10]

# 写法 2：filter + map + lambda（类似 Java Stream）
result2 = list(map(lambda x: x * 2, filter(lambda x: x > 0, nums)))

# 嵌套推导式：把每个字符串拆成字符再拼成一个大列表
words = ["hello", "world"]
chars = [ch for word in words for ch in word]  # ['h','e','l','l','o',...]

if __name__ == "__main__":
    print(result)
    print(result2)
    print(chars)
