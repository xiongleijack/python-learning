# pass：占位，什么都不做。循环体 / 分支不能空着时可以用它。
# while True:
#     pass

cmd = "start"
match cmd:
    case "start":
        print("starting...")
    case "stop":
        print("stopping...")
    case _:
        print("unknown")
