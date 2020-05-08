from xml.etree import ElementTree
import sys
import _test

if __name__ == "__main__":
    obstructed = None
    replay_moves = []
    xml = ElementTree.fromstring(open(sys.argv[1], "rb").read())
    for state in [
        z
        for x in xml if x.tag == "room"
        for y in x if y.tag == "data" and y.get("class") == "memento"
        for z in y if z.tag == "state"
    ]:
        if obstructed is None:
            obstructed = _test.gamestate.parse(state).board.obstructed
        else:
            for move in state:
                if move.tag == "lastMove":
                    movetype = move.get("class")
                    if movetype == "skipmove":
                        replay_moves.append(_test.moves.SkipMove())
                    elif movetype == "dragmove":
                        start = None
                        dest = None
                        for movetag in move:
                            if movetag.tag == "start":
                                start = (int(movetag.get("x")),
                                         int(movetag.get("y")))
                            elif movetag.tag == "destination":
                                dest = (int(movetag.get("x")),
                                        int(movetag.get("y")))
                        replay_moves.append(_test.moves.DragMove(start, dest))
                    elif movetype == "setmove":
                        piece = None
                        dest = None
                        for movetag in move:
                            if movetag.tag == "piece":
                                piece = (movetag.get("owner"),
                                         movetag.get("type"))
                            elif movetag.tag == "destination":
                                dest = (int(movetag.get("x")),
                                        int(movetag.get("y")))
                        replay_moves.append(_test.moves.SetMove(piece, dest))
    print(obstructed)
    print(*[str(x) for x in replay_moves], sep="\n")
