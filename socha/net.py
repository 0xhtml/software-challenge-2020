import socket
import threading
from xml.etree import ElementTree

from . import gamestate, moves, players


class Client:
    def __init__(self, host: str, port: int):
        self.room = None
        self.gamestate = None

        self.thread = None

        self.player = players.Random()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.send("<protocol>")

    def send(self, data: str):
        self.socket.send(data.encode())

    def send_move(self, move: moves.Move):
        print(move)
        data = f"<room roomId=\"{self.room}\">{move.to_xml()}</room>"
        self.send(data)

    def recv(self) -> bool:
        data = b""
        opened_tags = 0
        tags = 0
        while True:
            data += self.socket.recv(1)

            if len(data) < 2:
                continue

            if data[-2:] == b"</" or data[-2:] == b"/>":
                opened_tags -= 1
            elif data[-2] == 60:
                opened_tags += 1
                tags += 1

            if opened_tags == -1:
                return False

            if opened_tags != 0 or tags == 0:
                continue

            while not data.endswith(b">"):
                data += self.socket.recv(1)

            xml = ElementTree.fromstring(data)

            if xml.tag == "joined":
                self.room = xml.get("roomId")
                return True
            elif xml.tag == "room":
                xmldata = xml.find("data")
                xmlclass = xmldata.get("class")
                if xmlclass == "memento":
                    self.gamestate = gamestate.parse(xmldata.find("state"))
                elif xmlclass == "sc.framework.plugins.protocol.MoveRequest":
                    thread = threading.Thread(target=self.run_bot)
                    thread.start()

                    if self.thread is not None and self.thread.is_alive():
                        self.thread._stop()

                    self.thread = thread
                elif xmlclass == "error":
                    raise Exception(xmldata.get("message"))
                return True
            elif xml.tag == "left":
                return False
            elif xml.tag == "sc.protocol.responses.CloseConnection":
                return False
            else:
                print("unknown")
                return True

    def run_bot(self):
        self.send_move(self.player.get(self.gamestate))

    def join_any_game(self):
        self.send("<join gameType=\"swc_2020_hive\"/>")
        self.socket.recv(len(b"<protocol>\n  "))
        while self.recv():
            pass
        if self.thread is not None and self.thread.is_alive():
            self.thread._stop()
        self.socket.close()

    def join_reservation(self, reservation: str):
        pass
