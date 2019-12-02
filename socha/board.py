from xml.etree import ElementTree

from . import pos


class Board:
    def __init__(self, empty: set, obstructed: set, red: set, blue: set):
        self.empty = empty
        self.obstructed = obstructed
        self.red = red
        self.blue = blue
        self.both_fields = red.union(blue)

    def __str__(self) -> str:
        s = """
         XXXXXX
        XXXXXXX
       XXXXXXXX
      XXXXXXXXX
     XXXXXXXXXX
    XXXXXXXXXXX
     XXXXXXXXXX
      XXXXXXXXX
       XXXXXXXX
        XXXXXXX
         XXXXXX
        """
        positions = [
            (0,5),(1,4),(2,3),(3,2),(4,1),(5,0),(-1,5),(0,4),(1,3),(2,2),(3,1),
            (4,0),(5,-1),(-2,5),(-1,4),(0,3),(1,2),(2,1),(3,0),(4,-1),(5,-2),
            (-3,5),(-2,4),(-1,3),(0,2),(1,1),(2,0),(3,-1),(4,-2),(5,-3),(-4,5),
            (-3,4),(-2,3),(-1,2),(0,1),(1,0),(2,-1),(3,-2),(4,-3),(5,-4),(-5,5),
            (-4,4),(-3,3),(-2,2),(-1,1),(0,0),(1,-1),(2,-2),(3,-3),(4,-4),
            (5,-5),(-5,4),(-4,3),(-3,2),(-2,1),(-1,0),(0,-1),(1,-2),(2,-3),
            (3,-4),(4,-5),(-5,3),(-4,2),(-3,1),(-2,0),(-1,-1),(0,-2),(1,-3),
            (2,-4),(3,-5),(-5,2),(-4,1),(-3,0),(-2,-1),(-1,-2),(0,-3),(1,-4),
            (2,-5),(-5,1),(-4,0),(-3,-1),(-2,-2),(-1,-3),(0,-4),(1,-5),(-5,0),
            (-4,-1),(-3,-2),(-2,-3),(-1,-4),(0,-5)
        ]
        for position in positions:
            if position in self.empty:
                s = s.replace("X", "[]", 1)
            elif position in self.red:
                for position2 in self.red:
                    if position2 == position:
                        t = position2.pieces[-1][0]
                        break
                s = s.replace("X", "R" + t, 1)
            elif position in self.blue:
                for position2 in self.blue:
                    if position2 == position:
                        t = position2.pieces[-1][0]
                        break
                s = s.replace("X", "B" + t, 1)
            elif position in self.obstructed:
                s = s.replace("X", "OO", 1)
            else:
                s = s.replace("X", "  ", 1)
        return s


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
