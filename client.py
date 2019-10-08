import gamestate
import piece
import socket
from xml.etree import ElementTree


class Client:
    def __init__(self, host: str, port: int):
        self.room = None
        self.state = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.send('<protocol>')

    def send(self, data: str):
        self.socket.send(data.encode())
        print('send:', data.encode()[:100])

    def send_setmove(self, piece: piece.Piece, x: int, y: int, z: int):
        data = f"""
        <room roomId="{self.room}">
            <data class="setmove">
                <piece owner="{piece.color}" type="{piece.type}"/>
                <destination x="{x}" y="{y}" z="{z}"/>
            </data>
        </room>
        """
        self.send(data)

    def send_dragmove(self, sx: int, sy: int, sz: int, dx: int, dy: int, dz: int):
        data = f"""
        <room roomId="{self.room}">
            <data class="dragmove">
                <start x="{sx}" y="{sy}" z="{sz}"/>
                <destination x="{dx}" y="{dy}" z="{dz}"/>
            </data>
        </room>
        """
        self.send(data)

    def send_missmove(self):
        data = f"""
        <room roomId="{self.room}">
            <data class="missmove"/>
        </room>
        """
        self.send(data)

    def recv(self):
        data = b''
        while True:
            data += self.socket.recv(1024)

            try:
                xml = ElementTree.fromstring(data)
            except ElementTree.ParseError:
                continue

            print('recv:', data[:100])

            if xml.tag == 'joined':
                return self.parse_joined(xml)
            elif xml.tag == 'room':
                return self.parse_room(xml)
            elif xml.tag == 'left':
                return self.parse_left(xml)
            elif xml.tag == 'sc.protocol.responses.CloseConnection':
                return self.parse_close_connection(xml)
            else:
                print('unknown')
                return True

    def parse_joined(self, xml: ElementTree.Element):
        self.room = xml.get('roomId')
        return True

    def parse_room(self, xml: ElementTree.Element):
        xmldata = xml.find('data')
        if xmldata.get('class') == 'memento':
            self.state = gamestate.parse(xmldata.find('state'))
        elif xmldata.get('class') == 'sc.framework.plugins.protocol.MoveRequest':
            t = int(self.state.turn / 2)
            if not t:
                t = 0
            pos = (-t, 0, t)
            self.send_setmove(self.state.get_undeployed(self.state.color)[0], *pos)
        return True

    def parse_left(self, xml: ElementTree.Element):
        return False
    
    def parse_close_connection(self, xml: ElementTree.Element):
        return False

    def join_any_game(self):
        self.send('<join gameType="swc_2020_hive"/>')
        self.socket.recv(len(b'<protocol>\n  '))
        while self.recv():
            pass
        self.socket.close()

    def join_reservation(self, reservation: str):
        pass
