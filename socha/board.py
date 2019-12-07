from xml.etree import ElementTree


class Board:
    def __init__(self, fields: dict, obstructed: set):
        self.fields = fields
        self.obstructed = obstructed
        self.cache = {}

    def empty(self):
        if "empty" in self.cache:
            return self.cache["empty"].copy()
        empty = set()
        for pos in self.fields:
            if len(self.fields[pos]) == 0:
                empty.add(pos)
        self.cache["empty"] = empty
        return empty.copy()

    def nonempty(self):
        if "nonempty" in self.cache:
            return self.cache["nonempty"].copy()
        nonempty = set()
        for pos in self.fields:
            if len(self.fields[pos]) > 0:
                nonempty.add(pos)
        self.cache["nonempty"] = nonempty
        return nonempty.copy()

    def color(self, color: str):
        if "color" + color in self.cache:
            return self.cache["color" + color].copy()
        positions = set()
        for pos in self.fields:
            if len(self.fields[pos]) == 0:
                continue
            if self.fields[pos][-1][0] == color:
                positions.add(pos)
        self.cache["color" + color] = positions
        return positions.copy()


def parse(xml: ElementTree.Element) -> Board:
    fields = {}
    obstructed = set()
    for fields in xml.findall("fields"):
        for field in fields.findall("field"):
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
