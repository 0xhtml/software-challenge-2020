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

        if (self.turn > 5 and (self.color, "BEE") not in self.undeployed):
            types = {"BEE"}
        else:
            undeployed = filter(lambda x: x[0] == self.color, self.undeployed)
            types = {x[1] for x in undeployed}

        return {move.SetMove((self.color, x), y) for x in types for y in dests}


def parse(xml: ElementTree.Element):
    color = xml.get("currentPlayerColor")
    turn = int(xml.get("turn"))

    _board = board.parse(xml.find("board"))

    undeployed = []
    for xmlpiece in xml.findall("*/piece"):
        undeployed.append((xmlpiece.get('owner'), xmlpiece.get('type')))

    return GameState(color, turn, _board, undeployed)
