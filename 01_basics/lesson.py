"""
01 - 基础语法

Java          Python
int x = 1;    x = 1          # 动态类型，运行时决定类型
final int     无 final 关键字，约定用全大写常量名 MAX_SIZE = 100
String s      s: str = "hi"  # 类型标注可选，不强制
"""


def demo_types() -> None:
    age = 30
    price = 19.99
    name = "Alice"
    active = True
    nothing = None  # 类似 Java null

    print(type(age), type(price), type(name), type(active), type(nothing))


def demo_strings() -> None:
    # f-string ≈ Java 15+ 的 formatted string
    user = "Bob"
    print(f"Hello, {user}!")

    # 多行字符串
    sql = """
    SELECT id, name
    FROM users
    WHERE active = true
    """
    print(sql.strip())

    # 常用方法（类似 String API）
    text = "  daily-dev-tools  "
    print(text.strip().upper())


def demo_input_output() -> None:
    # 学习阶段可注释掉 input，避免阻塞自动化运行
    # answer = input("你几年 Java 经验？")
    # print(f"收到: {answer}")
    pass


if __name__ == "__main__":
    demo_types()
    demo_strings()
    demo_input_output()
