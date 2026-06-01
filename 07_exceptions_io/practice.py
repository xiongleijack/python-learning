"""练习：读取 JSON 文件为 dict，文件不存在返回 {}"""

import json
from pathlib import Path


def load_json(path: Path) -> dict:
    # TODO: try/except FileNotFoundError
    return {}


if __name__ == "__main__":
    missing = Path(__file__).with_name("not-exist.json")
    assert load_json(missing) == {}
    print("practice 07 通过 ✓（文件不存在分支）")
