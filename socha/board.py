from xml.etree import ElementTree


class Board:
    def __init__(self, fields: dict, obstructed: set):
        self.fields = fields
        self.obstructed = obstructed

    def empty(self):
        empty = set()
        for pos in self.fields:
            if len(self.fields[pos]) == 0:
                empty.add(pos)
        return empty

    def nonempty(self):
        nonempty = set()
        for pos in self.fields:
            if len(self.fields[pos]) > 0:
                nonempty.add(pos)
        return nonempty


    def color(self, color: str):
        positions = set()
        for pos in self.fields:
            if len(self.fields[pos]) == 0:
                continue
            if self.fields[pos][-1][0] == color:
                positions.add(pos)
        return positions


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
    return Board(empty, obstructed, red, blue)
