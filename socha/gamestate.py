from xml.etree import ElementTree

from . import board, moves


class GameState:
    def __init__(self, color: str, turn: int, board: board.Board, undeployed: set):
        self.color = color
        self.turn = turn
        self.board = board
        self.undeployed = undeployed

        a = (1, 0, -1)
        b = (1, -1, 0)
        c = (0, -1, 1)
        d = (-1, 0, 1)
        e = (-1, 1, 0)
        f = (0, 1, -1)
        self.directions = {a, b, c, d, e, f}

    def oppfields(self):
        color = "blue" if self.color == "RED" else "red"
        return self.board.__getattribute__(color)

    def ownfields(self):
        return self.board.__getattribute__(self.color.lower())

    def bothfields(self):
        return self.board.red.union(self.board.blue)

    def validfields(self):
        return self.board.red.union(self.board.blue).union(self.board.empty)

    def get_neighbours(self, pos: tuple):
        return {(pos[0] + x[0], pos[1] + x[1], pos[2] + x[2]) for x in self.directions}

    def get_possible_move_dests(self, dests):
        dests = {y for x in dests for y in self.get_neighbours(x)}
        dests = dests.intersection(self.board.empty)
        return dests

    def get_possible_set_moves(self):
        if self.turn == 0:
            dests = self.board.empty
        elif self.turn == 1:
            field = self.oppfields().__iter__().__next__()
            dests = self.get_neighbours(field)
            dests = dests.intersection(self.board.empty)
        else:
            dests = self.get_possible_move_dests(self.ownfields())

            def f(x):
                neighbours = self.get_neighbours(x)
                for neighbour in neighbours:
                    for oppfield in self.oppfields():
                        if neighbour == oppfield[:-1]:
                            return False
                return True
            dests = filter(f, dests)

        if (self.turn > 5 and (self.color, "BEE") in self.undeployed):
            types = {"BEE"}
        else:
            undeployed = filter(lambda x: x[0] == self.color, self.undeployed)
            types = {x[1] for x in undeployed}
            types = filter(lambda x: x == "GRASSHOPPER" or x == "BEE", types)

        return {moves.SetMove((self.color, y), x) for x in dests for y in types}

    def get_possible_drag_moves(self):
        if (self.color, "BEE") in self.undeployed:
            return set()

        possible_moves = set()
        validfields = {x[:3] for x in self.validfields()}

        for field in self.ownfields():
            neighbours = self.get_neighbours(field)
            bothfields_positions = {x[:-1] for x in self.bothfields()}
            neighbours = neighbours.intersection(bothfields_positions)

            def search(found, next):
                next = self.get_neighbours(next)
                next = next.difference(found)
                next = next.intersection(bothfields_positions)
                found.update(next)
                for snext in next:
                    found.update(search(found, snext))
                return found

            first = neighbours.pop()
            res = search({first, field[:-1]}, first)
            if len(res) < len(self.bothfields()):
                continue

            possible_dests = self.bothfields()
            possible_dests.discard(field)
            possible_dests = self.get_possible_move_dests(possible_dests)

            if field[3] == "BEE":
                dests = self.get_neighbours(field)
                dests = dests.intersection(possible_dests)
            elif field[3] == "BEETLE":
                possible_dests.update(self.bothfields())
                possible_dests.discard(field)
                dests = self.get_neighbours(field)
                dests = dests.intersection(possible_dests)
            elif field[3] == "SPIDER":
                dests = {field}
                all_dests = dests.copy()
                for _ in range(2):
                    dests = {y for x in dests for y in self.get_neighbours(x)}
                    dests = dests.intersection(possible_dests)
                    dests = dests.difference(all_dests)
                    all_dests.update(dests)
            elif field[3] == "ANT":
                dests = {field}
                while True:
                    ndests = {y for x in dests for y in self.get_neighbours(x)}
                    ndests = ndests.intersection(possible_dests)
                    l = len(dests)
                    dests.update(ndests)
                    if len(dests) == l:
                        break
                dests.discard(field)
            elif field[3] == "GRASSHOPPER":
                dests = set()
                for x, y, z in self.directions:
                    nfield = (field[0] + x, field[1] + y, field[2] + z)
                    if nfield in self.board.empty:
                        continue
                    while nfield not in self.board.empty and nfield in validfields:
                        nfield = (nfield[0] + x, nfield[1] + y, nfield[2] + z)
                    if nfield in validfields:
                        dests.add(nfield)

            possible_moves.update(moves.DragMove(field, x) for x in dests)

        return possible_moves


def parse(xml: ElementTree.Element):
    color = xml.get("currentPlayerColor")
    turn = int(xml.get("turn"))

    _board = board.parse(xml.find("board"))

    undeployed = []
    for xmlpiece in xml.findall("*/piece"):
        undeployed.append((xmlpiece.get("owner"), xmlpiece.get("type")))

    return GameState(color, turn, _board, undeployed)
