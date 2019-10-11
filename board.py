from xml.etree import ElementTree


class Board:
    def __init__(self, empty: set, obstructed: set, red: set, blue: set):
        self.empty = empty
        self.obstructed = obstructed
        self.red = red
        self.blue = blue

    def get_neighbours(self, pos: tuple):
        a = (1, 0, -1)
        b = (1, -1, 0)
        c = (0, -1, 1)
        d = (-1, 0, 1)
        e = (-1, 1, 0)
        f = (0, 1, -1)
        return {(pos[0] + x[0], pos[1] + x[1], pos[2] + x[2]) for x in {a, b, c, d, e, f}}

def parse(xml: ElementTree.Element):
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
                if xmlfield.find("piece") != None:
                    xmlpiece = xmlfield.find("piece")
                    if xmlpiece.get("owner") == "RED":
                        red.add((x, y, z, xmlpiece.get("type")))
                    else:
                        blue.add((x, y, z, xmlpiece.get("type")))
                else:
                    empty.add((x, y, z))
    return Board(empty, obstructed, red, blue)
