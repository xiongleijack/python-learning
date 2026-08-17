"""
02 - 控制流

关键差异：
- 用缩进代替 {}，通常 4 个空格
- elif 不是 else if
- for 直接遍历序列，没有 C 风格 for(int i=0; ...)
- match 类似 Java switch（Python 3.10+）
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

# --- for：直接遍历序列 ---
print("=== for 遍历序列 ===")
names = ["git", "ai", "permission"]
for name in names:
    print(name)
print("-" * 10)

print("=== for range ===")
# range(3) 得到 0,1,2，类似 for (int i = 0; i < 3; i++)
for i in range(3):
    print(i)
print("-" * 10)

# --- while ---
print("=== while ===")
n = 3
while n > 0:
    print(n)
    n -= 1
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
