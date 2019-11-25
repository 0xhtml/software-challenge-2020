class Pos():
    def __init__(self, x: int, y: int, t: str = None):
        self.x = x
        self.y = y
        self.z = (-x) + (-y)
        self.t = t

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        if self.t is not None:
            return f"({self.x}, {self.y}, {self.z}, \"{self.t}\")"
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        if isinstance(other, type(self)):
            if other.t is not None:
                return Pos(self.x + other.x, self.y + other.y)
            return Pos(self.x + other.x, self.y + other.y, self.t)
        if isinstance(other, tuple):
            return Pos(self.x + other[0], self.y + other[1], self.t)
        raise TypeError("unsupported operand type(s) for +")
