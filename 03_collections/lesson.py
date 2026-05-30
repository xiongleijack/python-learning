"""
03 - 集合

Java              Python
List<T>           list
Map<K,V>          dict
Set<T>            set
stream().map()    列表推导式 [f(x) for x in items]
Optional          常用 None + if 判断
"""


def demo_list() -> None:
    tools = ["git", "ai", "tags"]
    tools.append("permission")  # add
    print(tools[0], tools[-1])  # 支持负索引
    print(len(tools))


def demo_dict() -> None:
    # 类似 Map.of 但可变
    config = {
        "provider": "anthropic",
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
    }
    print(config["model"])
    print(config.get("timeout", 120))  # 带默认值，类似 getOrDefault


def demo_set() -> None:
    tags = {"java", "python", "python"}
    print(tags)  # 去重


def demo_comprehension() -> None:
    nums = [1, 2, 3, 4, 5]
    evens = [n for n in nums if n % 2 == 0]
    print(evens)  # [2, 4]

    upper = {k: v.upper() if isinstance(v, str) else v for k, v in {"a": "hi"}.items()}
    print(upper)


if __name__ == "__main__":
    demo_list()
    demo_dict()
    demo_set()
    demo_comprehension()
