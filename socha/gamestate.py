from xml.etree import ElementTree

from . import board, moves


class GameState:
    def __init__(self, c: str, t: int, b: board.Board, undep: list, m: list):
        self.color = c
        self.opp = "BLUE" if c == "RED" else "RED"
        self.turn = t
        self.board = b
        self.undeployed = undep
        self.moves = m
        self.directions = [
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, 0),
            (-1, 1),
            (0, 1)
        ]

    def get_neighbours(self, pos: tuple):
        return ((pos[0] + x[0], pos[1] + x[1]) for x in self.directions)

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
            dests = set(self.get_neighbours(field))
            dests.intersection_update(self.board.empty())
        else:
            dests = self.board.color(self.color)
            dests = {y for x in dests for y in self.get_neighbours(x)}
            dests.intersection_update(self.board.empty())

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
            types = (x[1] for x in undeployed)

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
            if len(self.board.fields[pos]) == 1:
                fields = self.board.nonempty()
                fields.discard(pos)
                if not self.is_connected(fields):
                    continue

            if self.board.fields[pos][-1][1] == "BEETLE":
                dests = self.get_beetle_move_dests(pos)
            elif self.board.fields[pos][-1][1] == "BEE":
                dests = self.get_bee_move_dests(pos, pos)
            elif self.board.fields[pos][-1][1] == "SPIDER":
                dests = self.get_spider_move_dests(pos)
            elif self.board.fields[pos][-1][1] == "ANT":
                dests = self.get_ant_move_dests(pos)
            elif self.board.fields[pos][-1][1] == "GRASSHOPPER":
                dests = self.get_grasshopper_move_dests(pos)
            else:
                continue

            possible_moves.update(moves.DragMove(pos, x) for x in dests)

        return possible_moves

    def get_beetle_move_dests(self, pos: tuple) -> set:
        # Get neighbours of pos
        neighbours = set(self.get_neighbours(pos))

        # If we are on top of another piece add it aswell
        if len(self.board.fields[pos]) > 1:
            neighbours.add(pos)

        # Only take fields with pieces
        neighbours.intersection_update(self.board.nonempty())

        # Get fields next to fields
        dests = {y for x in neighbours for y in self.get_neighbours(x)}

        # Only take fields in reach
        dests.intersection_update(self.get_neighbours(pos))

        # Only take valid fields
        dests.intersection_update(self.board.fields.keys())

        # Return fields
        return dests

    def get_bee_move_dests(self, pos: tuple, start_pos: tuple) -> set:
        # Get neighbours of pos
        neighbours = set(self.get_neighbours(pos))

        # Only take fields with pieces
        neighbours.intersection_update(self.board.nonempty())

        # Remove own field
        neighbours.discard(start_pos)

        # Get fields next to fields
        dests = set()
        for neighbour in neighbours:
            dests.symmetric_difference_update(self.get_neighbours(neighbour))

        # Get obstructed fields
        obstructed = self.board.obstructed.copy()

        # Only take obstructed fields in reach
        obstructed.intersection_update(self.get_neighbours(pos))

        # Get fields next to obscructed fields
        obstructed = (y for x in obstructed for y in self.get_neighbours(x))

        # Remove fields next to obstructed
        dests.difference_update(obstructed)

        # Only take fields in reach
        dests.intersection_update(self.get_neighbours(pos))

        # Only take empty fields
        dests.intersection_update(self.board.empty())

        # Return fields
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
        found = set()
        todo = {pos}
        while len(todo) > 0:
            dest = todo.pop()
            found.add(dest)
            dests = self.get_bee_move_dests(dest, pos)
            dests.difference_update(found)
            todo.update(dests)
        found.discard(pos)
        return found

    def get_grasshopper_move_dests(self, pos: tuple) -> set:
        dests = set()
        for direction in self.directions:
            dest = (pos[0] + direction[0], pos[1] + direction[1])
            if dest in self.board.empty():
                continue
            while dest in self.board.nonempty():
                dest = (dest[0] + direction[0], dest[1] + direction[1])
            dests.add(dest)
        dests.intersection_update(self.board.empty())
        return dests

    def around_bee(self, color: str) -> set:
        for field in self.board.fields:
            for piece in self.board.fields[field]:
                if piece == (color, "BEE"):
                    return set(self.get_neighbours(field))
        return set()

    def game_ended(self):
        if self.color != "RED":
            return False
        empty = self.board.empty()
        return self.around_bee(self.color).difference(empty) == 6 or \
            self.around_bee(self.opp).difference(empty) == 6 or \
            self.turn >= 60


def parse(xml: ElementTree.Element) -> GameState:
    color = xml.get("currentPlayerColor")
    turn = int(xml.get("turn"))

    _board = board.parse(xml.find("board"))

    undeployed = []
    for piece in xml.findall("*/piece"):
        undeployed.append((piece.get("owner"), piece.get("type")))

    return GameState(color, turn, _board, undeployed, [])
