from xml.etree import ElementTree


class Board:
    def __init__(self, fields: dict, obstructed: set):
        self.fields = fields
        self.obstructed = obstructed
        self.cache = {}

    def empty(self):
        if "empty" in self.cache:
            return self.cache["empty"].copy()
        empty = {x for x, y in self.fields.items() if y == []}
        self.cache["empty"] = empty
        return empty.copy()

    def nonempty(self):
        if "nonempty" in self.cache:
            return self.cache["nonempty"].copy()
        nonempty = {x for x, y in self.fields.items() if y != []}
        self.cache["nonempty"] = nonempty
        return nonempty.copy()

    def color(self, color: str):
        if "color" + color in self.cache:
            return self.cache["color" + color].copy()
        positions = {x for x, y in self.fields.items() if y != []
                     and y[-1][0] == color}
        self.cache["color" + color] = positions
        return positions.copy()

    def __hash__(self):
        return hash(frozenset((x, *self.fields[x]) for x in self.nonempty()))


def parse(xml: ElementTree.Element) -> Board:
    fields = {}
    obstructed = set()
    for field in xml.findall("fields/field"):
        x = int(field.get("x"))
        y = int(field.get("y"))
        if field.get("isObstructed") == "true":
            obstructed.add((x, y))
        else:
            pieces = []
            for piece in field:
                pieces.append((piece.get("owner"), piece.get("type")))
            fields[(x, y)] = pieces
    return Board(fields, obstructed)
