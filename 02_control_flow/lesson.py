"""
02 - 控制流

关键差异：
- 用缩进代替 {}，通常 4 个空格
- elif 不是 else if
- for 直接遍历序列，没有 C 风格 for(int i=0; ...)
- match 类似 Java switch（Python 3.10+）

怎么通关：
- 每小节先看示例，再在「练习」处自己写
- 从上往下运行本文件
- 打印「某关卡通关 ✓」= 过关；assert 报错 = 还没过，改完再跑
"""

# --- if / elif / else ---
print("=== if / elif / else ===")
score = 85
if score >= 90:
    level = "A"
elif score >= 80:
    level = "B"
else:
    level = "C"
print(level)
print("-" * 10)

# 练习 1（2 题）
# 题 1：score = 72，按上面规则得到 level
# 通关标准：level == "C"
score = 72
# TODO: 写 if / elif / else
assert level == "C", "题 1：72 分应该是 C"
print("if 题 1 通关 ✓")

# 题 2：score = 90，按上面规则得到 level
# 通关标准：level == "A"
score = 90
# TODO: 写 if / elif / else
assert level == "A", "题 2：90 分应该是 A"
print("if 关卡通关 ✓")
print("-" * 10)

# --- for：直接遍历序列 ---
print("=== for 遍历序列 ===")
names = ["git", "ai", "permission"]
for name in names:
    print(name)
print("-" * 10)

# 练习 2（2 题）
# 题 1：用 for 把 names 里的每个名字逐个放进 copied（不要写 copied = names）
# 通关标准：copied == ["git", "ai", "permission"]
copied = []
# TODO: for name in names: copied.append(name)

# 题 2：用 for 数 names 里有多少个名字，放到 count
# 通关标准：count == 3
count = 0
# TODO: for name in names: count += 1

assert copied == ["git", "ai", "permission"], "题 1：应用 for 把名字逐个 append 进 copied"
assert count == 3, "题 2：每循环一次 count += 1，最后应是 3"
print("for 遍历关卡通关 ✓")
print("-" * 10)

print("=== for range ===")
# range(3) 得到 0,1,2，类似 for (int i = 0; i < 3; i++)
for i in range(3):
    print(i)
print("-" * 10)

# 练习 3（2 题）
# 题 1：用 for + range 得到 0 到 4，放进 nums
# 通关标准：nums == [0, 1, 2, 3, 4]
nums = []
# TODO: for i in range(5): nums.append(i)

# 题 2：用 for + range 得到 1、2、3 的平方，放进 squares
# 通关标准：squares == [1, 4, 9]
squares = []
# TODO: for i in range(1, 4): squares.append(i * i)

assert nums == [0, 1, 2, 3, 4], "题 1：range(5) 是 0,1,2,3,4"
assert squares == [1, 4, 9], "题 2：range(1, 4) 是 1,2,3，再各自平方"
print("for range 关卡通关 ✓")
print("-" * 10)

# --- while ---
print("=== while ===")
# while 条件:
#     循环体
#     别忘了改条件，否则会死循环

# 练习 4（2 题）
# 题 1：用 while 从 3 倒数到 1，把数字依次放进 countdown
# 通关标准：countdown == [3, 2, 1]
countdown = []
n = 3
# TODO: while n > 0: 把 n 放进 countdown，然后 n -= 1

# 题 2：用 while 从 1 加到 5，把数字依次放进 up
# 通关标准：up == [1, 2, 3, 4, 5]
up = []
n = 1
# TODO: while n <= 5: 把 n 放进 up，然后 n += 1

assert countdown == [3, 2, 1], "题 1：从 3 倒数到 1"
assert up == [1, 2, 3, 4, 5], "题 2：从 1 加到 5"
print("while 关卡通关 ✓")
print("-" * 10)

# --- match（Python 3.10+），类似 Java switch ---
print("=== match ===")
cmd = "start"
match cmd:
    case "start":
        print("starting...")
    case "stop":
        print("stopping...")
    case _:
        print("unknown")
print("-" * 10)

# 练习 5（2 题）
# 题 1：cmd = "stop"，用 match 得到 action
# 通关标准：action == "stopping..."
cmd = "stop"
# TODO: match cmd，把对应字符串赋给 action
assert action == "stopping...", "题 1：stop 应对应 stopping..."
print("match 题 1 通关 ✓")

# 题 2：cmd = "pause"，没有对应分支，走默认 _
# 通关标准：action == "unknown"
cmd = "pause"
# TODO: 再写一次 match
assert action == "unknown", "题 2：pause 应走 case _，action == 'unknown'"  # pyright: ignore[reportUndefinedVariable]
print("match 关卡通关 ✓")
print("-" * 10)
print("02 控制流 全部通关 ✓")
