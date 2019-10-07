import socket
from xml.etree import ElementTree


class Client:
    def __init__(self, host, port):
        self.room = None
        self.color = None
        self.turn = None
        self.board = None
        self.undeployed = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.send(b'<protocol>')

    def send(self, data):
        self.socket.send(data)

    def recv(self):
        data = b''
        while True:
            data += self.socket.recv(1024)

            try:
                xml = ElementTree.fromstring(data)
            except ElementTree.ParseError:
                continue

            if xml.tag == 'joined':
                self.room = xml.get('roomId')
            elif xml.tag == 'room':
                xmldata = xml.find('data')
                if xmldata.get('class') == 'memento':
                    self.parse_state(xmldata.find('state'))
                elif xmldata.get('class') == 'sc.framework.plugins.protocol.MoveRequest':
                    self.send_move()
            elif xml.tag == 'left':
                return False

            return True

    def parse_state(self, xml):
        self.color = xml.get('currentPlayerColor')
        self.turn = xml.get('turn')

        xmlboard = xml.find('board')
        self.board = {}
        for xmlfields in xmlboard.findall('fields'):
            for xmlfield in xmlfields.findall('field'):
                x = xmlfield.get('x')
                y = xmlfield.get('y')
                z = xmlfield.get('z')
                if xmlfield.get('isObstructed') == 'true':
                    self.board[(x, y, z)] = 'OBSTRUCTED'
                else:
                    self.board[(x, y, z)] = 'EMPTY'

        self.undeployed = {'RED': [], 'BLUE': []}

        xmlundeployedRed = xml.find('undeployedRedPieces')
        for xmlpiece in xmlundeployedRed.findall('piece'):
            self.undeployed['RED'].append(xmlpiece.get('type'))

        xmlundeployedBlue = xml.find('undeployedBluePieces')
        for xmlpiece in xmlundeployedBlue.findall('piece'):
            self.undeployed['BLUE'].append(xmlpiece.get('type'))

    def send_move(self):
        ret = b'<room roomId="' + self.room.encode() + b'">'
        ret += b'<data class="setmove">'
        ret += b'<piece owner="' + self.color.encode() + b'" type="ANT"/>'
        ret += b'<destination x="0" y="0" z="0"/>'
        ret += b'</data>'
        ret += b'</room>'
        self.socket.send(ret)

    def join_any_game(self):
        self.send(b'<join gameType="swc_2020_hive"/>')
        self.socket.recv(len("<protocol>"))
        while self.recv():
            pass

    def join_reservation(self, reservation):
        pass
