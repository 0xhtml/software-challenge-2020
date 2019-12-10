from xml.etree import ElementTree

from . import board, moves


class GameState:
    def __init__(self, color: str, turn: int, board: board.Board, undep: set):
        self.color = color
        self.opp = "BLUE" if color == "RED" else "RED"
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

    def get_neighbours(self, pos: tuple) -> set:
        return {(pos[0] + x[0], pos[1] + x[1]) for x in self.directions}

    def is_connected(self, fields: set) -> bool:
        next = {fields.pop()}
        while len(next) > 0:
            next = {y for x in next for y in self.get_neighbours(x)}
            next.intersection_update(fields)
            fields.difference_update(next)
        return len(fields) == 0

    def get_possible_moves(self) -> set:
        possible_moves = self.get_possible_set_moves()
        possible_moves.update(self.get_possible_drag_moves())
        if len(possible_moves) == 0:
            possible_moves.add(moves.SkipMove())
        return possible_moves

    def get_possible_set_moves(self) -> set:
        if self.turn == 0:
            dests = self.board.empty()
        elif self.turn == 1:
            field = self.board.color(self.opp).pop()
            dests = self.get_neighbours(field)
            dests = dests.intersection(self.board.empty())
        else:
            dests = self.board.color(self.color)
            dests = {y for x in dests for y in self.get_neighbours(x)}
            dests = dests.intersection(self.board.empty())

            def f(x):
                neighbours = self.get_neighbours(x)
                for neighbour in neighbours:
                    for oppfield in self.board.color(self.opp):
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

        for pos in self.board.color(self.color):
            fields = self.board.nonempty()
            fields.discard(pos)
            if not self.is_connected(fields):
                continue

            if self.board.fields[pos][-1][1] == "BEETLE":
                dests = self.get_beetle_move_dests(pos, pos)
            elif self.board.fields[pos][-1][1] == "BEE":
                dests = self.get_bee_move_dests(pos, pos)
            elif self.board.fields[pos][-1][1] == "SPIDER":
                dests = self.get_spider_move_dests(pos)
            elif self.board.fields[pos][-1][1] == "ANT":
                dests = self.get_ant_move_dests(pos)
            elif self.board.fields[pos][-1][1] == "GRASSHOPPER":
                dests = self.get_grasshopper_move_dests(pos)
            else:
                dests = set()

            possible_moves.update(moves.DragMove(pos, x) for x in dests)

        return possible_moves

    def get_beetle_move_dests(self, pos: tuple, start_pos: tuple) -> set:
        fields = self.board.nonempty()
        fields.discard(start_pos)

        dests = {y for x in fields for y in self.get_neighbours(x)}
        dests.intersection_update(self.board.empty())
        dests.update(self.board.nonempty())
        dests.intersection_update(self.get_neighbours(pos))

        for i in range(6):
            a = (
                pos[0] + self.directions[i][0],
                pos[1] + self.directions[i][1]
            )
            b = (
                pos[0] + self.directions[(i + 1) % 6][0],
                pos[1] + self.directions[(i + 1) % 6][1]
            )
            c = (
                pos[0] + self.directions[(i + 2) % 6][0],
                pos[1] + self.directions[(i + 2) % 6][1]
            )
            if a not in fields and c not in fields:
                dests.discard(b)
        return dests

    def get_bee_move_dests(self, pos: tuple, start_pos: tuple) -> set:
        dests = self.get_beetle_move_dests(pos, start_pos)
        dests.intersection_update(self.board.empty())
        fields = self.board.nonempty()
        fields.discard(start_pos)
        fields.update(self.board.obstructed)
        for i in range(6):
            a = (
                pos[0] + self.directions[i][0],
                pos[1] + self.directions[i][1]
            )
            b = (
                pos[0] + self.directions[(i + 1) % 6][0],
                pos[1] + self.directions[(i + 1) % 6][1]
            )
            c = (
                pos[0] + self.directions[(i + 2) % 6][0],
                pos[1] + self.directions[(i + 2) % 6][1]
            )
            if a in fields and c in fields:
                dests.discard(b)
        return dests

    def get_spider_move_dests(self, pos: tuple) -> set:
        dests = {pos}
        all_dests = dests.copy()
        for _ in range(3):
            dests = {
                y
                for x in dests
                for y in self.get_bee_move_dests(x, pos)
            }
            dests.difference_update(all_dests)
            all_dests.update(dests)
        return dests

    def get_ant_move_dests(self, pos: tuple) -> set:
        dests = {pos}
        while True:
            ndests = {
                y
                for x in dests
                for y in self.get_bee_move_dests(x, pos)
            }
            count = len(dests)
            dests.update(ndests)
            if len(dests) == count:
                break
        dests.discard(pos)
        return dests

    def get_grasshopper_move_dests(self, pos: tuple) -> set:
        dests = set()
        for direction in self.directions:
            dest = (pos[0] + direction[0], pos[1] + direction[1])
            if dest in self.board.empty():
                continue
            while dest in self.board.nonempty():
                dest = (dest[0] + direction[0], dest[1] + direction[1])
                if dest in self.board.obstructed:
                    break
            dests.add(dest)
        dests.intersection_update(self.board.empty())
        return dests

    def pieces_around_bee(self, color: str) -> int:
        for field in self.board.fields:
            for piece in self.board.fields[field]:
                if piece == (color, "BEE"):
                    neighbours = self.get_neighbours(field)
                    neighbours.difference_update(self.board.empty())
                    return len(neighbours)
        return 10

    def clone(self):
        fields = {}
        for key in self.board.fields:
            fields[key] = self.board.fields[key].copy()
        _board = board.Board(
            fields,
            self.board.obstructed.copy()
        )
        return GameState(
            self.color,
            self.turn,
            _board,
            self.undeployed.copy()
        )


def parse(xml: ElementTree.Element) -> GameState:
    color = xml.get("currentPlayerColor")
    turn = int(xml.get("turn"))

    _board = board.parse(xml.find("board"))

    undeployed = []
    for piece in xml.findall("*/piece"):
        undeployed.append((piece.get("owner"), piece.get("type")))

    return GameState(color, turn, _board, undeployed)
