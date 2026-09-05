import asyncio
import time
from pathlib import Path


# 串行调度
def download(url):
    time.sleep(1)          # 模拟网络 I/O，阻塞当前线程
    return f"{url} 下载完成"

start = time.perf_counter()
for url in ["a", "b", "c"]:
    print(download(url))   # 3 秒才全部完成
print(f"耗时 {time.perf_counter() - start:.2f}s")  # 约 3.00s


# 并行调度
async def download(url):          # async = 声明这是协程
    await asyncio.sleep(1)        # asyncio = 模块，提供 sleep / gather
    return f"{url} 下载完成"


async def main():
    tasks = [download(url) for url in ["a", "b", "c"]]
    for result in await asyncio.gather(*tasks):
        print(result)


def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.strip()      # 逐行产出，而不是 readlines() 一次性全读进内存


def process(line: str) -> None:
    print(line)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    print(f"异步调度耗时 {time.perf_counter() - start:.2f}s")  # 约 1.00s

    sample = Path(__file__).with_name("sample.log")
    print("--- read_lines ---")
    for line in read_lines(sample):
        process(line)
