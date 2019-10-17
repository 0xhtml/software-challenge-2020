from xml.etree import ElementTree

from . import board, moves


class GameState:
    def __init__(self, color: str, turn: int, board: board.Board, undep: set):
        self.color = color
        self.turn = turn
        self.board = board
        self.undeployed = undep

    def oppfields(self) -> set:
        color = "blue" if self.color == "RED" else "red"
        return self.board.__getattribute__(color)

    def ownfields(self) -> set:
        return self.board.__getattribute__(self.color.lower())

    def bothfields(self) -> set:
        return self.board.red.union(self.board.blue)

    def get_neighbours(self, pos: tuple) -> set:
        a = (1, 0, -1)
        b = (1, -1, 0)
        c = (0, -1, 1)
        d = (-1, 0, 1)
        e = (-1, 1, 0)
        f = (0, 1, -1)
        return {
            (pos[0] + x[0], pos[1] + x[1], pos[2] + x[2])
            for x in {a, b, c, d, e, f}
        }

    def get_possible_move_dests(self, dests: set) -> set:
        dests = {y for x in dests for y in self.get_neighbours(x)}
        dests = dests.intersection(self.board.empty)
        return dests

    def get_possible_set_moves(self) -> set:
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

        return {
            moves.SetMove((self.color, y), x)
            for x in dests
            for y in types
        }

    def get_possible_drag_moves(self) -> set:
        if (self.color, "BEE") in self.undeployed:
            return set()

        possible_moves = set()

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
                # TODO: Filter out too tight fits
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
                    # TODO: Filter out too tight fits
                    all_dests.update(dests)
            elif field[3] == "ANT":
                dests = {field}
                while True:
                    ndests = {y for x in dests for y in self.get_neighbours(x)}
                    ndests = ndests.intersection(possible_dests)
                    # TODO: Filter out too tight fits
                    old_len = len(dests)
                    dests.update(ndests)
                    if len(dests) == old_len:
                        break
                dests.discard(field)
            elif field[3] == "GRASSHOPPER":
                dests = set()

            possible_moves.update(moves.DragMove(field, x) for x in dests)

        return possible_moves


def parse(xml: ElementTree.Element) -> GameState:
    color = xml.get("currentPlayerColor")
    turn = int(xml.get("turn"))

    _board = board.parse(xml.find("board"))

    undeployed = []
    for xmlpiece in xml.findall("*/piece"):
        undeployed.append((xmlpiece.get("owner"), xmlpiece.get("type")))

    return GameState(color, turn, _board, undeployed)
