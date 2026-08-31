"""
01 - LLM vs Agent

普通 LLM：一问一答，不会自己去查天气、跑 SQL。
Agent：模型 + 工具 + 循环，直到它决定「可以回答了」。

本文件不调真实 API，用假模型把循环跑给你看。
"""

print("*" * 10 + " 普通 LLM（没有工具） " + "*" * 10)
print("用户：上海今天几度？")
print("模型：我不知道实时天气。（编或拒答）")
print("-" * 10)

print("*" * 10 + " Agent 一圈 " + "*" * 10)


def get_weather(city: str) -> dict:
    return {"city": city, "temperature": 18, "condition": "cloudy"}


# 假模型：第一次要调工具，第二次拿到结果后才给最终回答
step = 0


def fake_llm(messages: list) -> dict:
    global step
    step += 1
    if step == 1:
        return {
            "type": "tool_call",
            "tool": "get_weather",
            "args": {"city": "上海"},
        }
    return {"type": "final", "text": "上海今天 18 度，阴天。"}


messages = [{"role": "user", "content": "上海今天几度？"}]
for i in range(5):
    out = fake_llm(messages)
    print(f"第 {i + 1} 轮模型输出：", out)
    if out["type"] == "final":
        print("最终回答：", out["text"])
        break
    if out["type"] == "tool_call":
        result = get_weather(**out["args"])
        print("  执行工具：", result)
        messages.append({"role": "tool", "content": str(result)})

print("-" * 10)
print("记住：Agent = 判断（模型）+ 动手（函数）+ 再判断（循环）。")
