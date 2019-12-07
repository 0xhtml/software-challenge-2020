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
    for xmlfields in xml.findall("fields"):
        for xmlfield in xmlfields.findall("field"):
            x = int(xmlfield.get("x"))
            y = int(xmlfield.get("y"))
            if xmlfield.get("isObstructed") == "true":
                obstructed.add((x, y))
            else:
                pieces = []
                owner = None
                for xmlpiece in xmlfield:
                    pieces.append((xmlpiece.get("owner"), xmlpiece.get("type")))
                fields[(x, y)] = pieces
    return Board(fields, obstructed)
