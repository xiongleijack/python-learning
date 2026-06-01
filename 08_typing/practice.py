"""练习：实现 first_or_default(items: list[int], default: int) -> int"""


def first_or_default(items: list[int], default: int) -> int:
    # TODO
    return default


if __name__ == "__main__":
    assert first_or_default([1, 2], 0) == 1
    assert first_or_default([], 42) == 42
    print("practice 08 通过 ✓")
