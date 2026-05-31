# while True:
#     pass

class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

def where_is(point: Point) -> str:
    match point:
        case Point(x=0, y=0):
            return "origin"
        case Point(x=0, y=y):
            return "y-axis"
        case Point(x=x, y=0):
            return "x-axis"
        case Point(x=x, y=y):
            return "other"


point = Point(0, 0)
print(where_is(point))