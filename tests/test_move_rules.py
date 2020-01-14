import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from socha import gamestate, board


def drag(fields: dict, dests: set, obs=set()):
    for x in range(-5, 6):
        if x >= 0:
            ys = range(-5, 6 - x)
        else:
            ys = range(-5 - x, 6)
        for y in ys:
            if (x, y) in obs:
                continue
            if (x, y) not in fields:
                fields[(x, y)] = []
            else:
                fields[(x, y)] = [("RED", x) for x in fields[(x, y)]]

    _board = board.Board(fields, obs)
    _gamestate = gamestate.GameState("RED", 10, _board, set(), [])
    possible_moves = _gamestate.get_possible_moves()

    for move in possible_moves:
        if move.start == (0, 0) and move.dest not in dests:
            raise Exception("Invalid move found: " + str(move))
        elif move.start == (0, 0) and move.dest in dests:
            dests.discard(move.dest)

    if len(dests) > 0:
        raise Exception("Missing move found: " + str(dests))

def test_basic1_move():
    drag(
        {
            (0, 0): ["BEE"],
            (0, 1): ["GRASSHOPPER"],
            (1, -1): ["SPIDER"],
            (2, -1): ["ANT"],
            (2, -2): ["ANT"],
            (0, -1): ["ANT"],
            (2, 0): ["BEETLE"],
            (1, 1): ["BEETLE"],
            (0, -1): ["BEETLE"],
            (2, -2): ["GRASSHOPPER"],
            (3, -3): ["BEE"]
        },
        {
            (-1, 0),
            (-1, 1)
        }
    )

def test_basic2_move():
    drag(
        {
            (0, 1): ["SPIDER"],
            (0, 0): ["BEETLE"],
            (2, -2): ["SPIDER"],
            (1, -2): ["BEETLE"],
            (1, 0): ["BEE"],
            (2, -1): ["BEE"],
        },
        {
            (-1, 1),
            (0, 1),
            (1, 0),
            (1, -1)
        },
        {
            (-2, 1)
        }
    )

def test_bee_move():
    drag(
        {
            (0, 0): ["BEE"],
            (-1, 0): ["GRASSHOPPER"],
            (-1, -1): ["SPIDER"],
            (0, -2): ["ANT"],
            (1, -2): ["BEETLE"],
            (1, 0): ["BEETLE"],
            (2, -1): ["GRASSHOPPER"],
            (2, -2): ["SPIDER"],
            (3, -3): ["BEE"]
        },
        {
            (-1, 1),
            (0, 1),
            (0, -1),
            (1, -1)
        },
        {
            (2, -3)
        }
    )

def test_beetle_move():
    drag(
        {
            (1, 0): ["BEE"],
            (0, 1): ["SPIDER"],
            (0, 0): ["BEETLE"],
            (-1, 1): ["SPIDER"],
            (-2, 0): ["BEE"],
            (-2, 1): ["ANT"]
        },
        {
            (1, 0),
            (1, -1),
            (0, 1),
            (-1, 0),
            (-1, 1)
        }
    )

def test_beetle2_move():
    drag(
        {
            (1, 0): ["BEE"],
            (0, 1): ["SPIDER"],
            (0, 0): ["ANT", "BEETLE"],
            (-1, 1): ["SPIDER"],
            (-2, 0): ["BEE"],
            (-2, 1): ["ANT"]
        },
        {
            (1, 0),
            (1, -1),
            (0, 1),
            (-1, 0),
            (-1, 1)
        }
    )


def test_grasshopper_move():
    drag(
        {
            (0, 0): ["GRASSHOPPER"],
            (-1, 0): ["SPIDER"],
            (0, -2): ["SPIDER"],
            (2, -2): ["SPIDER"],
            (2, 0): ["SPIDER"],
            (0, -1): ["ANT"],
            (1, -2): ["ANT"],
            (2, -1): ["BEETLE"],
            (3, 0): ["BEETLE"],
            (1, 1): ["BEETLE"],
            (1, 0): ["BEE"],
            (4, -1): ["BEE"]
        },
        {
            (-2, 0),
            (0, -3),
            (4, 0)
        }
    )

def test_grasshopper2_move():
    drag(
        {
            (-2, 0): ["BEE"],
            (-1, 0): ["BEE"],
            (0, 0): ["GRASSHOPPER"]
        },
        {
            (-3, 0)
        }
    )

def test_spider_move():
    drag(
        {
            (0, 0): ["SPIDER"],
            (0, -1): ["ANT"],
            (0, -2): ["GRASSHOPPER"],
            (-1, -2): ["ANT"],
            (-1, -3): ["ANT"],
            (-2, -2): ["BEETLE"],
            (-3, -1): ["GRASSHOPPER"],
            (-4, 0): ["ANT"],
            (-4, 1): ["BEE"],
            (-4, 2): ["ANT"],
            (-3, 1): ["GRASSHOPPER"],
            (-3, 2): ["BEE"],
            (-2, 1): ["BEETLE"],
        },
        {
            (1, -3),
            (-3, 0),
            (-2, -1),
            (-2, 2)
        },
        {
            (-4, 3)
        }
    )

def test_ant_move():
    drag(
        {
            (0, 0): ["ANT"],
            (-1, 0): ["BEE"],
            (0, -1): ["GRASSHOPPER"],
            (-1, -1): ["GRASSHOPPER"],
            (-1, -2): ["BEETLE"],
            (-3, -1): ["ANT"],
            (-4, 0): ["BEE"],
            (-3, 1): ["BEETLE"],
            (-4, 2): ["ANT"],
            (-4, 1): ["SPIDER"],
            (-2, 1): ["SPIDER"]
        },
        {
            (1, -1),
            (1, -2),
            (-1, 1),
            (-2, 2),
            (-3, 2),
            (-4, 3),
            (-5, 3),
            (-5, 2),
            (-5, 1),
            (-5, 0),
            (-4, -1),
            (-3, -2),
            (-2, -2),
            (-1, -3),
            (0, -3),
        },
        {
            (0, -2)
        }
    )

def test_skip_move():
    drag(
        {
            (0, 0): ["BEE"],
            (-1, 0): ["BEE"],
            (1, 0): ["BEE"]
        },
        set()
    )
