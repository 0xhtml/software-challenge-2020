from xml.etree import ElementTree


class Position:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class Field:
    def __init__(self, position: Position, state):
        self.position = position
        self.state = state

    def get_neighbours(self, fields):
        return fields[:2]


def parse(xml: ElementTree.Element):
    x = int(xml.get("x"))
    y = int(xml.get("y"))
    z = int(xml.get("z"))
    if xml.get("isObstructed") == "true":
        state = "OBSTRUCTED"
    else:
        state = "EMPTY"
    return Field(Position(x, y, z), state)
