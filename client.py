import socket
from xml.etree import ElementTree


class Client:
    def __init__(self, host, port):
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

            if xml.tag == 'room':
                xmldata = xml.find('data')
                if xmldata.get('class') == 'memento':
                    xmlstate = xmldata.find('state')
                    self.color = xmlstate.get('currentPlayerColor')
                    self.turn = xmlstate.get('turn')

                    xmlboard = xmlstate.find('board')
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

                    xmlundeployedRed = xmlstate.find('undeployedRedPieces')
                    for xmlpiece in xmlundeployedRed.findall('piece'):
                        self.undeployed['RED'].append(xmlpiece.get('type'))

                    xmlundeployedBlue = xmlstate.find('undeployedBluePieces')
                    for xmlpiece in xmlundeployedBlue.findall('piece'):
                        self.undeployed['BLUE'].append(xmlpiece.get('type'))
                    print(self.undeployed)
                elif xmldata.get('class') == 'sc.framework.plugins.protocol.MoveRequest':
                    print('Send move for', self.color)
            elif xml.tag == 'left':
                return False

            return True

    def join_any_game(self):
        self.send(b'<join gameType="swc_2020_hive"/>')
        self.socket.recv(len("<protocol>"))
        while self.recv():
            pass

    def join_reservation(self, reservation):
        pass
