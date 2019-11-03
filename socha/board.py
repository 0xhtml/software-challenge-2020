from xml.etree import ElementTree


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
            z = int(xmlfield.get("z"))
            if xmlfield.get("isObstructed") == "true":
                obstructed.add((x, y, z))
            else:
                if xmlfield.find("piece") is not None:
                    xmlpiece = xmlfield.find("piece")
                    if xmlpiece.get("owner") == "RED":
                        red.add((x, y, z, xmlpiece.get("type")))
                    else:
                        blue.add((x, y, z, xmlpiece.get("type")))
                else:
                    empty.add((x, y, z))
    return Board(empty, obstructed, red, blue)
