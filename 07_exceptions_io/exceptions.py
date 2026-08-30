"""
07 - 异常处理

Java                         Python
try { } catch (E e) { }      try: ... except E as e:
throw e                      raise          # except 里原样再抛
throw new E("msg")           raise E("msg")
finally                      finally
try-with-resources           with ...
"""

print("*" * 10 + " 1. try / except " + "*" * 10)

try:
    print("1" + 2)  # TypeError：str 不能和 int 相加（Java 会把 2 转成 "2"）
except TypeError as e:
    print("接到了:", type(e).__name__, e)

print("*" * 10 + " 2. 多种 except，先写具体再写宽的 " + "*" * 10)

for raw in ["10", "abc"]:
    try:
        n = int(raw)  # "abc" 会 ValueError
        print(raw, "->", n)
    except ValueError as e:
        print("不是合法整数:", e)
    except Exception as e:
        print("其它错误:", e)

print("*" * 10 + " 3. else / finally " + "*" * 10)

try:
    x = 10 / 2
except ZeroDivisionError:
    print("除零了")
else:
    print("没出错才走 else, x =", x)  # 类似「catch 没进」
finally:
    print("反正都会走 finally")

print("*" * 10 + " 4. raise = throw " + "*" * 10)


def must_positive(n: int) -> int:
    if n <= 0:
        raise ValueError(f"必须 > 0，收到 {n}")  # throw new ValueError(...)
    return n


try:
    must_positive(-1)
except ValueError as e:
    print("校验失败:", e)
    # raise  # 打开这行 = 看完再抛给外面

print("*" * 10 + " 5. 不要写成 except: " + "*" * 10)
print("光秃 except: 会连 Ctrl+C 一起吃掉。写成 except Exception as e:")

print("*" * 10 + " 6. with 里抛错，__exit__ 照样跑 " + "*" * 10)


class DemoLock:
    def __enter__(self):
        print("加锁")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("解锁, 异常类型 =", exc_type)
        return False  # False：异常继续往外抛


try:
    with DemoLock():
        raise RuntimeError("boom")
except RuntimeError as e:
    print("外面接到:", e)


# --- 练习（自己写，不要看答案） ---
# 题 1：parse_int(s) —— 能转成 int 就返回，否则返回 None
# 通关：parse_int("7") == 7 且 parse_int("x") is None
def parse_int(s: str) -> int | None:
    # TODO: try / except ValueError
    return -1


# 题 2：写一个自己的异常类 PositiveError，继承 Exception
# must_positive2(n) 在 n<=0 时 raise PositiveError
# class PositiveError(Exception):
#     ...


if __name__ == "__main__":
    if parse_int("7") == 7 and parse_int("x") is None:
        print("题 1 通关 ✓")
    else:
        print("题 1 还没过：去改 parse_int")
    print("题 2 写完自己 raise / except 试一下")
