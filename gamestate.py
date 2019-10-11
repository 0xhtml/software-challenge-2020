import board
import move
from xml.etree import ElementTree


class GameState:
    def __init__(self, color: str, turn: int, board: board.Board, undeployed: set):
        self.color = color
        self.turn = turn
        self.board = board
        self.undeployed = undeployed
        if color == "RED":
            self.own = self.board.red
            self.opp = self.board.blue
        else:
            self.own = self.board.blue
            self.opp = self.board.red

    def get_possible_set_moves(self):
        if self.turn == 0:
            dests = self.board.empty
        elif self.turn == 1:
            field = self.opp.__iter__().__next__()
            dests = self.board.get_neighbours(field)
            dests.intersection(self.board.empty)
        else:
            dests = {y for x in self.own for y in self.board.get_neighbours(x)}
            dests = dests.intersection(self.board.empty)
            def f(x):
                neighbours = self.board.get_neighbours(x)
                for neighbour in neighbours:
                    for oppfield in self.opp:
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
