"""
04 - 函数

Java                              Python
public static int add(int a, int b)    def add(a: int, b: int) -> int:
{ return a + b; }                      return a + b
void                                   -> None（也可省略，默认返回 None）
String... args                         *args
没有内置命名参数                        name="Ada"  /  def f(*, port=80)
重载多个同名方法                        一个函数 + 默认参数

怎么通关：
- 每小节先看示例，再补 TODO
- 从上往下运行本文件
- 打印「某关卡通关 ✓」= 过关；assert 报错 = 还没过
"""


# --- 1. 定义与返回 ---
print("=== 定义与返回 ===")

# Java: public static int add(int a, int b) { return a + b; }
def add(a: int, b: int) -> int:
    return a + b


print(add(2, 3))
print("-" * 10)

# 练习 1（2 题）
# 题 1：写 double(n)，返回 n 的 2 倍。通关：double(6) == 12
def double(n: int) -> int:
    # TODO
    return 0


# 题 2：写 greet(name)，返回 "Hello, {name}"。通关：greet("Java") == "Hello, Java"
def greet(name: str) -> str:
    # TODO
    return ""


assert double(6) == 12, "题 1 未通过"
assert greet("Java") == "Hello, Java", "题 2 未通过"
print("定义与返回 关卡通关 ✓")
print("-" * 10)


# --- 2. 默认参数（Java 里常靠重载） ---
print("=== 默认参数 ===")

def repeat(text: str, times: int = 2) -> str:
    return text * times


print(repeat("na"))       # 用默认 times=2 → nana
print(repeat("na", 3))    # nana na? → nanana
print("-" * 10)

# 练习 2（2 题）
# 题 1：写 power(base, exp=2)，默认求平方。
# 通关：power(5) == 25 且 power(2, 10) == 1024
def power(base: int, exp: int = 2) -> int:
    # TODO
    return 0


# 题 2：写 clamp(n, lo=0, hi=100)，把 n 限制在 [lo, hi]。
# 通关：clamp(150) == 100 且 clamp(-3, lo=-10, hi=10) == -3
def clamp(n: int, lo: int = 0, hi: int = 100) -> int:
    # TODO
    return 0


assert power(5) == 25, "题 1 未通过"
assert power(2, 10) == 1024, "题 1 未通过"
assert clamp(150) == 100, "题 2 未通过"
assert clamp(-3, lo=-10, hi=10) == -3, "题 2 未通过"
print("默认参数 关卡通关 ✓")
print("-" * 10)


# --- 3. 关键字参数 / 仅关键字参数 ---
print("=== 关键字参数 ===")

# Java 只能按位置传：log("hi", "ERROR")
# Python 可以按名字传，顺序可换：
def log(message: str, *, level: str = "INFO") -> None:
    """* 后面的参数必须写成 level="ERROR"，不能 log("hi", "ERROR")"""
    print(f"[{level}] {message}")


log("server started")
log("error happened", level="ERROR")
print("-" * 10)

# 练习 3（2 题）
# 题 1：用关键字参数调用 clamp，把 7 限制到 [1, 5]。
# 通关：clamped == 5
clamped = 0
# TODO

assert clamped == 5, "题 1 未通过"
print("关键字 题 1 通关 ✓")

# 题 2：写 connect(host, *, port=8080)，返回 "host:port"
# 通关：connect("localhost") == "localhost:8080"
#       connect("db", port=5432) == "db:5432"
def connect(host: str, *, port: int = 8080) -> str:
    # TODO
    return ""

assert connect("localhost") == "localhost:8080", "题 2 未通过"
assert connect("db", port=5432) == "db:5432", "题 2 未通过"
print("关键字参数 关卡通关 ✓")
print("-" * 10)


# --- 4. *args（类似 Java 可变参数 String...） ---
print("=== *args ===")

def summarize(*values: int) -> tuple[int, float]:
    return sum(values), sum(values) / len(values)


print(summarize(10, 20, 30))
print("-" * 10)

# 练习 4（2 题）
# 题 1：写 total(*nums)，返回所有数字之和。
# 通关：total(1, 2, 3, 4) == 10
def total(*nums: int) -> int:
    # TODO
    return 0


# 题 2：调用时把列表拆开。values = [10, 20, 30]，用 * 传给 total。
# Java 没有这种「调用处拆包」。通关：unpacked == 60
values = [10, 20, 30]
unpacked = 0
# TODO

assert total(1, 2, 3, 4) == 10, "题 1 未通过"
assert unpacked == 60, "题 2 未通过"
print("*args 关卡通关 ✓")
print("-" * 10)


# --- 5. **kwargs（把关键字参数收成 dict，Java 里常写成 Map） ---
print("=== **kwargs ===")

def add_many_kwargs(**kwargs: int) -> int:
    return sum(kwargs.values())


print(add_many_kwargs(a=1, b=2, c=3))
print("-" * 10)

# 练习 5（2 题）
# 题 1：写 label(**info)，返回 "{name} ({role})"。
# 通关：label(name="Ada", role="dev") == "Ada (dev)"
def label(**info: str) -> str:
    # TODO
    return ""


# 题 2：调用时把 dict 拆开。通关：labeled == "Bob (qa)"
person = {"name": "Bob", "role": "qa"}
labeled = ""
# TODO

assert label(name="Ada", role="dev") == "Ada (dev)", "题 1 未通过"
assert labeled == "Bob (qa)", "题 2 未通过"
print("**kwargs 关卡通关 ✓")
print("-" * 10)


# --- 6. 多返回值（其实是返回 tuple，Java 得自己建类/数组） ---
print("=== 多返回值 ===")

def minmax(a: int, b: int) -> tuple[int, int]:
    if a < b:
        return a, b
    return b, a


lo, hi = minmax(9, 3)  # 解包，类似同时接两个返回值
print(lo, hi)
print("-" * 10)

# 练习 6（2 题）
# 题 1：写 head_tail(items)，返回 (第一项, 剩下的列表)。
# 通关：head_tail([1, 2, 3]) == (1, [2, 3])
def head_tail(items: list[int]) -> tuple[int, list[int]]:
    # TODO
    return 0, []


# 题 2：写 divmod_like(a, b)，返回 (商, 余数)。
# 通关：divmod_like(17, 5) == (3, 2)
def divmod_like(a: int, b: int) -> tuple[int, int]:
    # TODO
    return 0, 0


assert head_tail([1, 2, 3]) == (1, [2, 3]), "题 1 未通过"
assert divmod_like(17, 5) == (3, 2), "题 2 未通过"
print("多返回值 关卡通关 ✓")
print("-" * 10)


# --- 7. 函数当值（Java 的 Function / 方法引用） ---
print("=== 函数当值 ===")

# 函数名可以当值传来传去，类似 Java 把方法引用传给 map
print(double)  # 打印的是函数本身，还没调用
print("-" * 10)

# 练习 7（2 题）
# 题 1：写 apply_twice(fn, x)，把 fn 对 x 用两次。
# 通关：apply_twice(double, 5) == 20
def apply_twice(fn, x):
    # TODO
    return x


# 题 2：写 my_map(fn, items)，对列表每一项调用 fn，收集结果。
# 通关：my_map(double, [1, 2, 3]) == [2, 4, 6]
def my_map(fn, items: list[int]) -> list[int]:
    result: list[int] = []
    # TODO
    return result


assert apply_twice(double, 5) == 20, "题 1 未通过"
assert my_map(double, [1, 2, 3]) == [2, 4, 6], "题 2 未通过"
print("函数当值 关卡通关 ✓")
print("-" * 10)


# --- 8. 可变默认参数陷阱（Python 特有，Java 没有这个坑） ---
print("=== 可变默认参数 ===")

# 错误示范：默认参数只求值一次，列表会被所有调用共享
def broken_add(item, bucket=[]):  # noqa: B006
    bucket.append(item)
    return bucket


print("broken 第1次:", broken_add("a"))
print("broken 第2次:", broken_add("b"))  # 会变成 ['a', 'b']，不是 ['b']
print("-" * 10)

# 练习 8（1 题，两个断言）
# 写 add_todo(item, todos=None)，把 item 放进列表后返回。
# 通关：两次独立调用互不影响（不要踩上面 broken_add 的坑）
def add_todo(item: str, todos: list[str] | None = None) -> list[str]:
    # TODO
    return []


first = add_todo("read")
second = add_todo("write")
assert first == ["read"], "第1次调用应只有 read"
assert second == ["write"], "第2次应只有 write；如果是 [read, write]，说明默认参数用了 []"
print("可变默认参数 关卡通关 ✓")
print("-" * 10)


# --- 模块：本文件当脚本跑 ---
# Java 的 public static void main
# Python：if __name__ == "__main__":  被 import 时不执行这块
if __name__ == "__main__":
    from pathlib import Path

    print("当前文件:", Path(__file__).name)
    print("04 函数 全部通关 ✓")
