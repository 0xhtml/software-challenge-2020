import os
import sys
import socket
import subprocess
import random
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from socha import players, gamestate, board, net


def noprint(*a, **b):
    pass


players.print = noprint
net.print = noprint


def create_gamestate() -> gamestate.GameState:
    undep = [
        ("RED", "BEE"),
        ("RED", "SPIDER"),
        ("RED", "SPIDER"),
        ("RED", "SPIDER"),
        ("RED", "GRASSHOPPER"),
        ("RED", "GRASSHOPPER"),
        ("RED", "BEETLE"),
        ("RED", "BEETLE"),
        ("RED", "ANT"),
        ("RED", "ANT"),
        ("RED", "ANT"),
        ("BLUE", "BEE"),
        ("BLUE", "SPIDER"),
        ("BLUE", "SPIDER"),
        ("BLUE", "SPIDER"),
        ("BLUE", "GRASSHOPPER"),
        ("BLUE", "GRASSHOPPER"),
        ("BLUE", "BEETLE"),
        ("BLUE", "BEETLE"),
        ("BLUE", "ANT"),
        ("BLUE", "ANT"),
        ("BLUE", "ANT"),
    ]
    fields = {}
    for x in range(-5, 6):
        if x >= 0:
            ys = range(-5, 6 - x)
        else:
            ys = range(-5 - x, 6)
        for y in ys:
            fields[(x, y)] = []
    obstructed = set()
    for _ in range(3):
        pos = random.choice(list(fields.keys()))
        del fields[pos]
        obstructed.add(pos)
    _board = board.Board(fields, obstructed)
    return gamestate.GameState("RED", 0, _board, undep)


def run_local(red: players.AlphaBeta, blue: players.AlphaBeta, x, start: bool) -> tuple:
    _gamestate = create_gamestate()

    redp = red() if start else blue()
    bluep = blue() if start else red()

    if start:
        redp.x = x
    else:
        bluep.x = x

    while True:
        move = redp.get(_gamestate)
        move.do(_gamestate)

        move = bluep.get(_gamestate)
        move.do(_gamestate)

        if _gamestate.game_ended():
            break

    _gamestate.color = "RED" if start else "BLUE"
    _gamestate.opponent = "BLUE" if start else "RED"
    return players.AlphaBeta().evaluate(_gamestate)


def popen(cmd: str) -> subprocess.Popen:
    p = subprocess.Popen(
        cmd.split(),
        cwd="../server",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    try:
        p.wait(2)
        raise Exception(cmd + " didn't start")
    except subprocess.TimeoutExpired:
        return p


def run_server(player: players.AlphaBeta, start: bool) -> tuple:
    s = socket.socket()
    s.connect(("localhost", 13050))
    s.send(b"""<protocol>
    <authenticate password="examplepassword" />
    <prepare gameType="swc_2020_hive">
        <slot displayName="a" />
        <slot displayName="b" />
    </prepare>""")
    r = s.recv(2048).decode().split("\n")
    a = r[2][r[2].find("<reservation>")+13:][:36]
    b = r[3][r[3].find("<reservation>")+13:][:36]

    p = popen("java -jar 1.jar -r " + (b if start else a))

    s.close()
    try:
        client = net.Client("localhost", 13050)
        client.player = player()
        client.join_reservation(a if start else b)
    finally:
        p.kill()

    client.gamestate.color = "RED" if start else "BLUE"
    client.gamestate.opp = "BLUE" if start else "RED"
    return players.AlphaBeta().evaluate(client.gamestate)


def test(count: int, func, args: tuple) -> tuple:
    evals = []

    for i in range(count):
        evals.append(func(*(args + (bool(i % 2),))))

    wins = [1 if x > 0 else 0 if x < 0 else 0.5 for x in evals]
    return sum(evals) / len(evals), sum(wins) / len(wins)
