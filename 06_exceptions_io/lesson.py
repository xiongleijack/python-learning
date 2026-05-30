"""
06 - 异常与文件

Java try-catch-finally     try-except-finally
IOException                  FileNotFoundError 等
Files.readString             with open(...) as f:
"""

import json
from pathlib import Path


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except OSError as exc:
        raise RuntimeError(f"读取失败: {path}") from exc


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def demo_with() -> None:
    # with 自动 close，类似 try-with-resources
    sample = Path(__file__).with_name("sample.json")
    write_json(sample, {"hello": "python"})
    print(read_text_safe(sample))


if __name__ == "__main__":
    demo_with()
