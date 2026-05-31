# 将用户输入的字符串打印三次
input_str = input("请输入一个字符串: ")
for _ in range(3):
    print(f"第{_ + 1}次打印: ")
    print(input_str)
    print("-" * 10)
