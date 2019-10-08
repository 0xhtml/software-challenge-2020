import piece
import field
import move
from xml.etree import ElementTree


class GameState:
    def __init__(self):
        self.color = None
        self.turn = None
        self.board = None
        self.undeployed = None

    def get_undeployed(self, color: str):
        undeployed = []
        for piece in self.undeployed:
            if piece.color == color:
                undeployed.append(piece)
        return undeployed

    def get_deployed(self, color: str):
        deployed = []
        for field in self.board:
            if isinstance(field.state, piece.Piece) and field.state.color == color:
                deployed.append(field)
        return deployed

    def get_empty_fields(self):
        return filter(lambda x: x.state == "EMPTY", self.board)

    def get_possible_set_moves(self):
        undeployed = self.get_undeployed(self.color)
        empty = self.get_empty_fields()
        if self.turn == 0:
            return [move.SetMove(x, y) for x in undeployed for y in empty]
        elif self.turn == 1:
            field = self.get_deployed("BLUE" if self.color == "RED" else "RED")[0]
            neighbours = field.get_neighbours(empty)
            return [move.SetMove(x, y) for x in undeployed for y in neighbours]
        else:
            return []


def parse(xml: ElementTree.Element):
    state = GameState()
    state.color = xml.get("currentPlayerColor")
    state.turn = int(xml.get("turn"))

    xmlboard = xml.find("board")
    state.board = []
    for xmlfields in xmlboard.findall("fields"):
        for xmlfield in xmlfields.findall("field"):
            state.board.append(field.parse(xmlfield))

    state.undeployed = []
    for xmlpiece in xml.findall("*/piece"):
        state.undeployed.append(piece.parse(xmlpiece))

    return state
