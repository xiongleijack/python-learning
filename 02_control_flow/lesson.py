"""
02 - 控制流

关键差异：
- 用缩进代替 {}，通常 4 个空格
- elif 不是 else if
- for 直接遍历序列，没有 C 风格 for(int i=0; ...)
"""


def demo_if() -> None:
    score = 85
    if score >= 90:
        level = "A"
    elif score >= 80:
        level = "B"
    else:
        level = "C"
    print(level)


def demo_for() -> None:
    names = ["git", "ai", "permission"]
    for name in names:
        print(name)

    for i in range(3):  # 0,1,2 类似 for(int i=0; i<3; i++)
        print(i)


def demo_while() -> None:
    n = 3
    while n > 0:
        print(n)
        n -= 1


def demo_match() -> None:  # Python 3.10+，类似 Java switch 表达式
    cmd = "start"
    match cmd:
        case "start":
            print("starting...")
        case "stop":
            print("stopping...")
        case _:
            print("unknown")


if __name__ == "__main__":
    demo_if()
    demo_for()
    demo_while()
    demo_match()
