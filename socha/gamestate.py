from xml.etree import ElementTree

from . import board, moves, pos


class GameState:
    def __init__(self, color: str, turn: int, board: board.Board, undep: set):
        self.color = color
        self.turn = turn
        self.board = board
        self.undeployed = undep
        self.directions = [
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, 0),
            (-1, 1),
            (0, 1)
        ]

    def oppfields(self) -> set:
        color = "blue" if self.color == "RED" else "red"
        return self.board.__getattribute__(color)

    def ownfields(self) -> set:
        return self.board.__getattribute__(self.color.lower())

    def bothfields(self) -> set:
        return self.board.red.union(self.board.blue)

    def validfields(self) -> set:
        return self.board.red.union(self.board.blue).union(self.board.empty)

    def get_neighbours(self, pos: pos.Pos) -> set:
        return {pos + x for x in self.directions}

    def is_connected(self, fields: set) -> bool:
        next = {fields.pop()}
        while len(next) > 0:
            next = {y for x in next for y in self.get_neighbours(x)}
            next.intersection_update(fields)
            fields.difference_update(next)
        return len(fields) == 0

    def get_possible_move_dests(self, dests: set) -> set:
        dests = {y for x in dests for y in self.get_neighbours(x)}
        dests = dests.difference(self.board.obstructed)
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
            dests = dests.intersection(self.board.empty)

            def f(x):
                neighbours = self.get_neighbours(x)
                for neighbour in neighbours:
                    for oppfield in self.oppfields():
                        if neighbour == oppfield:
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
            fields = self.bothfields()
            fields.discard(field)
            if not self.is_connected(fields):
                continue

            if field.t == "BEETLE":
                dests = self.get_beetle_move_dests(field)
            elif field.t == "BEE":
                dests = self.get_bee_move_dests(field)
            elif field.t == "SPIDER":
                dests = self.get_spider_move_dests(field)
            elif field.t == "ANT":
                dests = self.get_ant_move_dests(field)
            else:
                dests = set()

            possible_moves.update(moves.DragMove(field, x) for x in dests)

        return possible_moves

    def get_beetle_move_dests(self, field: tuple) -> set:
        dests = self.get_neighbours(field)
        possible_dests = self.bothfields()
        possible_dests.discard(field)
        possible_dests.update(self.get_possible_move_dests(possible_dests))
        dests.intersection_update(possible_dests)
        return dests

    def get_bee_move_dests(self, field: tuple) -> set:
        dests = self.get_beetle_move_dests(field)
        dests.intersection_update(self.board.empty)
        for i in range(6):
            a = field + self.directions[i]
            b = field + self.directions[(i + 1) % 6]
            c = field + self.directions[(i + 2) % 6]
            if a not in self.board.empty and c not in self.board.empty:
                dests.discard(b)
        return dests

    def get_spider_move_dests(self, field: tuple) -> set:
        dests = {field}
        all_dests = dests.copy()
        for _ in range(2):
            dests = {y for x in dests for y in self.get_bee_move_dests(x)}
            dests.difference_update(all_dests)
            all_dests.update(dests)
        return dests

    def get_ant_move_dests(self, field: tuple) -> set:
        dests = {field}
        while True:
            ndests = {y for x in dests for y in self.get_bee_move_dests(x)}
            l = len(dests)
            dests.update(ndests)
            if len(dests) == l:
                break
        dests.discard(field)
        return dests


def parse(xml: ElementTree.Element) -> GameState:
    color = xml.get("currentPlayerColor")
    turn = int(xml.get("turn"))

    _board = board.parse(xml.find("board"))

    undeployed = []
    for xmlpiece in xml.findall("*/piece"):
        undeployed.append((xmlpiece.get("owner"), xmlpiece.get("type")))

    return GameState(color, turn, _board, undeployed)
