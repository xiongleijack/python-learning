import asyncio

async def agent_task(name, delay):
    await asyncio.sleep(delay)
    return f"{name} 完成"

async def main():
    tasks = [
        agent_task("搜索", 3),
        agent_task("分析", 1),
        agent_task("写作", 2),
    ]
    # 用什么方法让先完成的先打印？
    for result in asyncio.as_completed(tasks):
        result = await result
        print(result)

if __name__ == "__main__":
    asyncio.run(main())