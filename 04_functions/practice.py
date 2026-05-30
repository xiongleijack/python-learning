"""练习：实现 clamp(value, low, high)，把 value 限制在 [low, high]"""


def clamp(value: int, low: int, high: int) -> int:
    # TODO
    return value


if __name__ == "__main__":
    assert clamp(5, 1, 10) == 5
    assert clamp(-1, 0, 10) == 0
    assert clamp(99, 0, 10) == 10
    print("practice 04 通过 ✓")
