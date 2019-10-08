import piece
import field
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


def parse(xml: ElementTree.Element):
    state = GameState()
    state.color = xml.get('currentPlayerColor')
    state.turn = int(xml.get('turn'))

    xmlboard = xml.find('board')
    state.board = []
    for xmlfields in xmlboard.findall('fields'):
        for xmlfield in xmlfields.findall('field'):
            state.board.append(field.parse(xmlfield))

    state.undeployed = []
    for xmlpiece in xml.findall('*/piece'):
        state.undeployed.append(piece.parse(xmlpiece))

    return state
