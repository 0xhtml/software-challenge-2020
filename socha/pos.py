class Pos():
    def __init__(self, x: int, y: int, pieces: list = None):
        self.x = x
        self.y = y
        self.z = (-x) + (-y)
        self.pieces = pieces

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        return False

    def __hash__(self) -> int:
        return (self.x, self.y).__hash__()

    def __str__(self) -> str:
        if self.pieces is not None:
            return f"({self.x}, {self.y}, {self.pieces})"
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, type(self)):
            return Pos(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple):
            return Pos(self.x + other[0], self.y + other[1])
        raise TypeError("unsupported operand type(s) for +")
