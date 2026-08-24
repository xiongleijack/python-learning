from ast import main


def front_back(str):
  if len(str) <= 1:
    return str
  a = str[0]
  print(a)
  b = str[-1]
  print(b)
  c = str[1:len(str) - 1]
  print(c)
  return a + b + c


def str_practice(str):
    print(str[0])
    print(str[1])
    print(str[-1])
    print(str[1:-1])

if __name__ == "__main__":
    # front_back("abcd")
    str_practice("xionglei")