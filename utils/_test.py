import os
import sys
import socket
import subprocess
import random
import threading
from multiprocessing import Queue
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
    _gamestate = gamestate.GameState("RED", 0, _board, undep)
    # moves.SetMove(("RED", "BEE"), (-4, 0)).do(_gamestate)
    # moves.SetMove(("BLUE", "BEE"), (-4, -1)).do(_gamestate)
    # moves.SetMove(("RED", "SPIDER"), (-4, 1)).do(_gamestate)
    # moves.DragMove((-4, -1), (-3, -1)).do(_gamestate)
    return _gamestate


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
    return players.AlphaBeta().evaluate(_gamestate), _gamestate.turn


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

    p = popen("java -jar " + str(int(i % 4 > 1)) + ".jar -r " + (b if i % 2 else a))

    s.close()
    try:
        client = net.Client("localhost", 13050)
        client.player = player()
        client.player.x = x
        client.join_reservation(a if i % 2 else b)
    finally:
        p.kill()

    client.gamestate.color = "RED" if i % 2 else "BLUE"
    client.gamestate.opp = "BLUE" if i % 2 else "RED"
    return players.AlphaBeta().evaluate(client.gamestate)


def worker(work: Queue, data: Queue, func, args: tuple):
    while not work.empty():
        _work = work.get()
        try:
            _data = func(*(args + _work))
            data.put((_data, _work[0]))
        except Exception as e:
            print(e.with_traceback())


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
    while not work.empty() or not data.empty():
        print("[" + ("=" * round(i / xcount * 100)) + ">" + (" " * (100 - round(i / xcount * 100))) + "]", end="\r")
        _data = data.get()
        xdata[_data[1]].append(_data[0])
        f = open("data.txt", "w")
        f.write(str(xdata))
        f.close()
        i += 1

    for thread in threads:
        thread.join()
        i += 1
        print("[" + ("=" * round(i / xcount * 100)) + ">" + (" " * (100 - round(i / xcount * 100))) + "]", end="\r")

    while not data.empty():
        _data = data.get()
        xdata[_data[1]].append(_data[0])

    evals = {y: [z[0] for z in xdata[y]] for y in x}
    turns = {y: [z[1] for z in xdata[y]] for y in x}
    return [(sum(evals[y]) / len(evals[y]), sum(turns[y]) / len(turns[y]), sum([1 if x > 0 else 0 if x < 0 else 0.5 for x in evals[y]]) / len(evals[y])) for y in x]
