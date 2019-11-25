from xml.etree import ElementTree

from . import pos


class Board:
    def __init__(self, empty: set, obstructed: set, red: set, blue: set):
        self.empty = empty
        self.obstructed = obstructed
        self.red = red
        self.blue = blue


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
                    xmlpiece = xmlfield.find("piece")
                    if xmlpiece.get("owner") == "RED":
                        red.add(pos.Pos(x, y, xmlpiece.get("type")))
                    else:
                        blue.add(pos.Pos(x, y, xmlpiece.get("type")))
                else:
                    empty.add(pos.Pos(x, y))
    return Board(empty, obstructed, red, blue)
