import bot
import gamestate
import move
import socket
from xml.etree import ElementTree


class Client:
    def __init__(self, host: str, port: int):
        self.room = None
        self.gamestate = None

        self.bot = bot.Bot()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.send('<protocol>')

    def send(self, data: str):
        self.socket.send(data.encode())

    def send_move(self, move: move.Move):
        data = f"<room roomId=\"{self.room}\">{move.to_xml()}</room>"
        self.send(data)

    def recv(self):
        data = b''
        while True:
            data += self.socket.recv(1024)

            try:
                xml = ElementTree.fromstring(data)
            except ElementTree.ParseError:
                continue

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
            self.gamestate = gamestate.parse(xmldata.find('state'))
        elif xmldata.get('class') == 'sc.framework.plugins.protocol.MoveRequest':
            self.send_move(self.bot.get(self.gamestate))
        elif xmldata.get('class') == "error":
            print(xmldata.get("message"))
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
