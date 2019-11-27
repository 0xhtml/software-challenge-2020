import socket
import threading
from xml.etree import ElementTree

from . import gamestate, moves, players, log


class Client:
    def __init__(self, host: str, port: int):
        self.room = None
        self.gamestate = None

        self.thread = None

        log.info("Using random player")
        self.player = players.Random()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(0.1)
        self.socket.connect((host, port))
        self.send("<protocol>")

    def send(self, data: str):
        self.socket.send(data.encode())

    def send_move(self, move: moves.Move):
        log.info(f"Send move {move}")
        data = f"<room roomId=\"{self.room}\">{move.__xml__()}</room>"
        self.send(data)

    def recv(self) -> bool:
        data = b""

        while True:
            try:
                data += self.socket.recv(1024)
            except socket.timeout:
                break

        if len(data) == 0:
            return True

        if not data.startswith(b"<protocol>"):
            data = b"<protocol>" + data
        if not data.endswith(b"</protocol>"):
            data += b"</protocol>"

        xml = ElementTree.fromstring(data)

        for tag in xml:
            if tag.tag == "joined":
                self.room = tag.get("roomId")
            elif tag.tag == "room":
                tagdata = tag.find("data")
                tagclass = tagdata.get("class")
                if tagclass == "memento":
                    self.gamestate = gamestate.parse(tagdata.find("state"))
                elif tagclass == "sc.framework.plugins.protocol.MoveRequest":
                    thread = threading.Thread(target=self.run_bot)
                    thread.start()

                    if self.thread is not None and self.thread.is_alive():
                        self.thread._stop()

                    self.thread = thread
                elif tagclass == "error":
                    log.error(tagdata.get("message"))
                else:
                    log.debug(f"Unknown tag <room class=\"{tagclass}\">")
            elif tag.tag == "left":
                log.debug("<left>")
                return False
            elif tag.tag == "sc.protocol.responses.CloseConnection":
                log.debug("<sc.protocol.responses.CloseConnection>")
                return False
            else:
                print(data)
                log.debug(f"Unknown tag <{tag.tag}>")

        return True

    def run_bot(self):
        self.send_move(self.player.get(self.gamestate))

    def join_any_game(self):
        log.info("Joining any game")
        self.send("<join gameType=\"swc_2020_hive\"/>")
        while self.recv():
            pass

    def join_reservation(self, reservation: str):
        log.info("Joining reservation")
        pass

    def stop(self):
        self.send("</protocol>\r\n")
        self.socket.close()
