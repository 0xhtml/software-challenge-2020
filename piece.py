from xml.etree import ElementTree

class Piece:
    def __init__(self, color: str, type: str):
        self.color = color
        self.type = type


def parse(xml: ElementTree.Element):
    return Piece(xml.get('owner'), xml.get('type'))
