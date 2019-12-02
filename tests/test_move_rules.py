import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from socha import gamestate, board, pos


def drag(pieces, dests, obs=set()):
    empty = set()
    for x in range(-5, 6):
        if x >= 0:
            ys = range(-5, 6 - x)
        else:
            ys = range(-5 - x, 6)
        for y in ys:
            _pos = pos.Pos(x, y)
            if _pos not in pieces and _pos not in obs:
                empty.add(_pos)

    _board = board.Board(empty, obs, pieces, set())
    _gamestate = gamestate.GameState("RED", 10, _board, set())
    possible_moves = _gamestate.get_possible_drag_moves()
    [print(x) for x in possible_moves]

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
            pos.Pos(0, 0, ["BEE"]),
            pos.Pos(0, 1, ["GRASSHOPPER"]),
            pos.Pos(1, -1, ["SPIDER"]),
            pos.Pos(2, -1, ["ANT"]),
            pos.Pos(2, -2, ["ANT"]),
            pos.Pos(0, -1, ["ANT"]),
            pos.Pos(2, 0, ["BEETLE"]),
            pos.Pos(1, 1, ["BEETLE"]),
            pos.Pos(0, -1, ["BEETLE"]),
            pos.Pos(2, -2, ["GRASSHOPPER"]),
            pos.Pos(3, -3, ["BEE"])
        },
        {
            (-1, 0),
            (-1, 1)
        }
    )

def test_basic2_move():
    drag(
        {
            pos.Pos(0, 0, ["BEETLE"]),
            pos.Pos(0, 1, ["SPIDER"]),
            pos.Pos(2, -2, ["SPIDER"]),
            pos.Pos(1, -2, ["BEETLE"]),
            pos.Pos(1, 0, ["BEE"]),
            pos.Pos(2, -1, ["BEE"])
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
            pos.Pos(0, 0, ["BEE"]),
            pos.Pos(-1, 0, ["GRASSHOPPER"]),
            pos.Pos(-1, -1, ["SPIDER"]),
            pos.Pos(0, -2, ["ANT"]),
            pos.Pos(1, -2, ["BEETLE"]),
            pos.Pos(1, 0, ["BEETLE"]),
            pos.Pos(2, -1, ["GRASSHOPPER"]),
            pos.Pos(2, -2, ["SPIDER"]),
            pos.Pos(3, -3, ["BEE"])
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
            pos.Pos(1, 0, ["BEE"]),
            pos.Pos(0, 1, ["SPIDER"]),
            pos.Pos(0, 0, ["BEETLE"]),
            pos.Pos(-1, 1, ["SPIDER"]),
            pos.Pos(-2, 0, ["BEE"]),
            pos.Pos(-2, 1, ["ANT"])
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
            pos.Pos(0, 0, ["GRASSHOPPER"]),
            pos.Pos(-1, 0, ["SPIDER"]),
            pos.Pos(0, -2, ["SPIDER"]),
            pos.Pos(2, -2, ["SPIDER"]),
            pos.Pos(2, 0, ["SPIDER"]),
            pos.Pos(0, -1, ["ANT"]),
            pos.Pos(1, -2, ["ANT"]),
            pos.Pos(2, -1, ["BEETLE"]),
            pos.Pos(3, 0, ["BEETLE"]),
            pos.Pos(1, 1, ["BEETLE"]),
            pos.Pos(1, 0, ["BEE"]),
            pos.Pos(4, -1, ["BEE"])
        },
        {
            (-2, 0),
            (0, -3),
            (4, 0)
        }
    )

def test_spider_move():
    drag(
        {
            pos.Pos(0, 0, ["SPIDER"]),
            pos.Pos(0, -1, ["ANT"]),
            pos.Pos(0, -2, ["GRASSHOPPER"]),
            pos.Pos(-1, -2, ["ANT"]),
            pos.Pos(-1, -3, ["ANT"]),
            pos.Pos(-2, -2, ["BEETLE"]),
            pos.Pos(-3, -1, ["GRASSHOPPER"]),
            pos.Pos(-4, 0, ["ANT"]),
            pos.Pos(-4, 1, ["BEE"]),
            pos.Pos(-4, 2, ["ANT"]),
            pos.Pos(-3, 1, ["GRASSHOPPER"]),
            pos.Pos(-3, 2, ["BEE"]),
            pos.Pos(-2, 1, ["BEETLE"]),
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
            pos.Pos(0, 0, ["ANT"]),
            pos.Pos(-1, 0, ["BEE"]),
            pos.Pos(0, -1, ["GRASSHOPPER"]),
            pos.Pos(-1, -1, ["GRASSHOPPER"]),
            pos.Pos(-1, -2, ["BEETLE"]),
            pos.Pos(-3, -1, ["ANT"]),
            pos.Pos(-4, 0, ["BEE"]),
            pos.Pos(-3, 1, ["BEETLE"]),
            pos.Pos(-4, 2, ["ANT"]),
            pos.Pos(-4, 1, ["SPIDER"]),
            pos.Pos(-2, 1, ["SPIDER"])
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
