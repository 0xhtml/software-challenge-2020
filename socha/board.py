from xml.etree import ElementTree

from . import pos


class Board:
    def __init__(self, empty: set, obstructed: set, red: set, blue: set):
        self.empty = empty
        self.obstructed = obstructed
        self.red = red
        self.blue = blue
        self.both_fields = red.union(blue)


def parse(xml: ElementTree.Element) -> Board:
    empty = set()
    obstructed = set()
    red = set()
    blue = set()
    for xmlfields in xml.findall("fields"):
        for xmlfield in xmlfields.findall("field"):
            x = int(xmlfield.get("x"))
            y = int(xmlfield.get("y"))
            if xmlfield.get("isObstructed") == "true":
                obstructed.add(pos.Pos(x, y))
            else:
                if xmlfield.find("piece") is not None:
                    pieces = []
                    owner = None
                    for xmlpiece in xmlfield:
                        owner = xmlpiece.get("owner")
                        pieces.append(xmlpiece.get("type"))
                    if owner == "RED":
                        red.add(pos.Pos(x, y, pieces))
                    else:
                        blue.add(pos.Pos(x, y, pieces))
                else:
                    empty.add(pos.Pos(x, y))
    return Board(empty, obstructed, red, blue)
