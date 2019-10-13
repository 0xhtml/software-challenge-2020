import bot
import gamestate
import move
import socket
from xml.etree import ElementTree
import time
import threading


class Client:
    def __init__(self, host: str, port: int):
        self.room = None
        self.gamestate = None

        self.file = f"data/{str(hex(int(time.time()*1000)))[-8:]}.xml"
        self.thread = None

        self.bot = bot.Bot()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.send("<protocol>")

    def send(self, data: str):
        self.socket.send(data.encode())

    def send_move(self, move: move.Move):
        print(move)
        data = f"<room roomId=\"{self.room}\">{move.to_xml()}</room>"
        self.send(data)

    def recv(self):
        data = b""
        while True:
            data += self.socket.recv(1024)

            try:
                xml = ElementTree.fromstring(data)
            except ElementTree.ParseError:
                continue

            if xml.tag == "joined":
                self.room = xml.get("roomId")
                return True
            elif xml.tag == "room":
                xmldata = xml.find("data")
                if xmldata.get("class") == "memento":
                    f = open(self.file, "wb")
                    f.write(data)
                    f.close()
                    self.gamestate = gamestate.parse(xmldata.find("state"))
                elif xmldata.get("class") == "sc.framework.plugins.protocol.MoveRequest":
                    thread = threading.Thread(target=self.run_bot)
                    thread.start()

                    if self.thread != None and self.thread.is_alive():
                        self.thread._stop()

                    self.thread = thread
                elif xmldata.get("class") == "error":
                    print(xmldata.get("message"))
                return True
            elif xml.tag == "left":
                return False
            elif xml.tag == "sc.protocol.responses.CloseConnection":
                return False
            else:
                print("unknown")
                return True

    def run_bot(self):
        self.send_move(self.bot.get(self.gamestate))

    def join_any_game(self):
        self.send("<join gameType=\"swc_2020_hive\"/>")
        self.socket.recv(len(b"<protocol>\n  "))
        while self.recv():
            pass
        if self.thread != None and self.thread.is_alive():
            self.thread._stop()
        self.socket.close()

    def join_reservation(self, reservation: str):
        pass
