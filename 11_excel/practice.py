"""
练习：实现 split_excel，将大 Excel 按指定行数拆成多个小文件。

要求（与 lesson.py 一致）：
  1. 只处理第一个工作表
  2. 第 1 行是表头，每个输出文件都要带表头
  3. rows_per_file 只限制「数据行」数量
  4. 输出文件名：{源文件名}_part001.xlsx, _part002.xlsx, ...
  5. rows_per_file <= 0 时 raise ValueError

验证：
  python 11_excel/practice.py

参考答案：solution.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_CHAPTER = Path(__file__).resolve().parent
if str(_CHAPTER) not in sys.path:
    sys.path.insert(0, str(_CHAPTER))

from lesson import create_sample_excel


def split_excel(source: Path, output_dir: Path, rows_per_file: int) -> list[Path]:
    # TODO: 使用 openpyxl 实现
    raise NotImplementedError


if __name__ == "__main__":
    base = Path(__file__).parent
    sample = base / "samples" / "practice_source.xlsx"
    out_dir = base / "output" / "practice"

    create_sample_excel(sample, data_rows=25)
    parts = split_excel(sample, out_dir, rows_per_file=10)

    assert len(parts) == 3, f"25 行按 10 行拆分应为 3 个文件，实际 {len(parts)}"
    assert parts[0].name == "practice_source_part001.xlsx"
    print("practice 11 通过 ✓")
    for p in parts:
        print(f"  生成: {p}")
