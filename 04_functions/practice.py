def add(a,b):
    return a + b

def add_new(a: int, b: int) -> int:
    return a + b

def add_many(*args):
    return sum(args)

def add_many_kwargs(**kwargs):
    return sum(kwargs.values())

print(add(1, 2))
print(add_many(1, 2, 3, 4, 5))
print(add_many_kwargs(a=1, b=2, c=3))


input_str = input("请输入一个字符串: ")