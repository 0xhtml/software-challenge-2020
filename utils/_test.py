import os
import sys
import socket
import subprocess
import random
import threading
import csocha
from multiprocessing import Queue
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from socha import players, gamestate, board, net, moves


def noprint(*a, **b):
    pass


# players.print = noprint
net.print = noprint


def create_gamestate(obstructed=set()) -> gamestate.GameState:
    undep = [
        (color, piece)
        for color in ["RED", "BLUE"]
        for piece in [
            "BEE",
            "SPIDER", "SPIDER", "SPIDER",
            "GRASSHOPPER", "GRASSHOPPER",
            "BEETLE", "BEETLE",
            "ANT", "ANT", "ANT"
        ]
    ]

    fields = {}
    for x in range(-5, 6):
        if x >= 0:
            ys = range(-5, 6 - x)
        else:
            ys = range(-5 - x, 6)
        for y in ys:
            fields[(x, y)] = []

    while len(obstructed) < 3:
        pos = random.choice(list(fields.keys()))
        del fields[pos]
        obstructed.add(pos)

    _board = board.Board(fields, obstructed)
    return gamestate.GameState("RED", 0, _board, undep)


class Random(players.AlphaBeta):
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        return random.choice(list(gamestate.get_possible_moves()))


def evaluate(gamestate: gamestate.GameState, color: str) -> int:
    empty = gamestate.board.empty()
    ownbee = gamestate.get_bee(color) or (7, 7)
    own = set(csocha.neighbours(ownbee)).intersection(empty)
    oppcolor = "BLUE" if color == "RED" else "RED"
    oppbee = gamestate.get_bee(oppcolor) or (7, 7)
    opp = set(csocha.neighbours(oppbee)).intersection(empty)
    return len(own) - len(opp)


def run_local(red: players.AlphaBeta, blue: players.AlphaBeta, x, i: int):
    _gamestate = create_gamestate()

    redp = red() if i % 2 else blue()
    bluep = blue() if i % 2 else red()
    redp.x = x
    bluep.x = x

    while True:
        move = redp.get(_gamestate)
        move.do(_gamestate)

        move = bluep.get(_gamestate)
        move.do(_gamestate)

        if _gamestate.game_ended():
            break

    value = evaluate(_gamestate, "RED" if i % 2 else "BLUE")
    win = 0.5 if value == 0 else 1 if value > 0 else 0
    return value, _gamestate.turn, win


def popen(cmd: str) -> subprocess.Popen:
    p = subprocess.Popen(
        cmd.split(),
        cwd="server",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    try:
        p.wait(2)
        raise Exception(cmd + " didn't start")
    except subprocess.TimeoutExpired:
        return p


def run_server(player: players.AlphaBeta, x: int, i: int) -> tuple:
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

    p = popen("java -jar " + str(int(i % 4 > 1)) +
              ".jar -r " + (b if i % 2 else a))

    s.close()
    try:
        client = net.Client("localhost", 13050)
        client.player = player()
        client.player.x = x
        client.join_reservation(a if i % 2 else b)
    finally:
        p.kill()

    value = evaluate(client.gamestate, "RED" if i % 2 else "BLUE")
    win = 0.5 if value == 0 else 1 if value > 0 else 0
    return value, client.gamestate.turn, win


def worker(work: Queue, data: Queue, func, args: tuple):
    while not work.empty():
        _work = work.get()
        try:
            _data = func(*(args + _work))
            data.put((_data, _work[0]))
        except Exception as e:
            print(e)


def progressbar(i, count):
    def printc(c):
        print(c, end="")
    printc("[")
    for _ in range(round(i / count * 100)):
        printc("=")
    printc(">")
    for _ in range(100 - round(i / count * 100)):
        printc(" ")
    printc("]")
    printc("\r")


def test(count: int, x, func, args: tuple) -> tuple:
    work = Queue()
    for y in x:
        for i in range(count):
            work.put((y, i))

    data = Queue()
    threads = []
    for _ in range(4):
        thread = threading.Thread(target=worker, args=(work, data, func, args))
        threads.append(thread)
        thread.start()

    i = 0
    xdata = {y: [] for y in x}
    xcount = len(x) * count
    progressbar(i, xcount)
    while not work.empty() or not data.empty():
        _data = data.get()
        xdata[_data[1]].append(_data[0])
        i += 1
        progressbar(i, xcount)

    for thread in threads:
        thread.join()
        if not data.empty():
            _data = data.get()
            xdata[_data[1]].append(_data[0])
            i += 1
            progressbar(i, xcount)

    evals = {y: [z[0] for z in xdata[y]] for y in x}
    turns = {y: [z[1] for z in xdata[y]] for y in x}
    wins = {y: [z[2] for z in xdata[y]] for y in x}
    return [
        (
            sum(evals[y]) / len(evals[y]),
            sum(turns[y]) / len(turns[y]),
            sum(wins[y]) / len(wins[y])
        ) for y in x
    ]
