import board
import move
from xml.etree import ElementTree


class GameState:
    def __init__(self, color: str, turn: int, board: board.Board, undeployed: set):
        self.color = color
        self.turn = turn
        self.board = board
        self.undeployed = undeployed

    def oppfields(self):
        color = "blue" if self.color == "RED" else "red"
        return self.board.__getattribute__(color)

    def ownfields(self):
        return self.board.__getattribute__(self.color.lower())

    def get_possible_move_dests(self, dests):
        dests = {y for x in dests for y in self.board.get_neighbours(x)}
        dests = dests.intersection(self.board.empty)
        return dests

    def get_possible_set_moves(self):
        if self.turn == 0:
            dests = self.board.empty
        elif self.turn == 1:
            field = self.oppfields().__iter__().__next__()
            dests = self.board.get_neighbours(field)
            dests = dests.intersection(self.board.empty)
        else:
            dests = self.ownfields()
            dests = {y for x in dests for y in self.board.get_neighbours(x)}
            dests = dests.intersection(self.board.empty)

            def f(x):
                neighbours = self.board.get_neighbours(x)
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

        return {move.SetMove((self.color, x), y) for x in types for y in dests}

    def get_possible_drag_moves(self):
        if (self.color, "BEE") in self.undeployed:
            return set()

        moves = set()

        for field in self.ownfields():
            possible_dests = self.board.red.union(self.board.blue)
            possible_dests.discard(field)
            possible_dests = self.get_possible_move_dests(possible_dests)

            if field[3] == "BEE":
                dests = self.board.get_neighbours(field)
                dests = dests.intersection(possible_dests)
            elif field[3] == "BEETLE":
                dests = set()
            elif field[3] == "SPIDER":
                all_dests = dests.copy()
                for _ in range(2):
                    dests = {
                        y for x in dests for y in self.board.get_neighbours(x)}
                    dests = dests.intersection(possible_dests)
                    dests = dests.difference(all_dests)
                    # TODO: Filter out too tight fits
                    all_dests.update(dests)
            elif field[3] == "ANT":
                dests = set()
            elif field[3] == "GRASSHOPPER":
                dests = set()

            moves.update(move.DragMove(field, x) for x in dests)

        return moves


def parse(xml: ElementTree.Element):
    color = xml.get("currentPlayerColor")
    turn = int(xml.get("turn"))

    _board = board.parse(xml.find("board"))

    undeployed = []
    for xmlpiece in xml.findall("*/piece"):
        undeployed.append((xmlpiece.get('owner'), xmlpiece.get('type')))

    return GameState(color, turn, _board, undeployed)
