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
        self.socket.connect((host, port))
        self.send("<protocol>")

    def send(self, data: str):
        self.socket.send(data.encode())

    def send_move(self, move: moves.Move):
        log.debug(self.gamestate.board)
        log.info(f"Send move {move}")
        data = f"<room roomId=\"{self.room}\">{move.__xml__()}</room>"
        self.send(data)

    def recv(self):
        done = False
        while not done:
            data = b""
            while True:
                data += self.socket.recv(1048576)  # 1MB

                if not data.startswith(b"<protocol>"):
                    full_data = b"<protocol>" + data
                else:
                    full_data = data

                if not data.endswith(b"</protocol>"):
                    full_data += b"</protocol>"
                else:
                    done = True

                try:
                    xml = ElementTree.fromstring(full_data)
                    log.debug(data[:200])
                    break
                except ElementTree.ParseError:
                    log.debug("Stopped receving too early")
                    pass

            self.parse(xml)

    def parse(self, xml: ElementTree.Element):
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
                self.send("<sc.protocol.responses.CloseConnection />")
                self.send("</protocol>")
            elif tag.tag == "sc.protocol.responses.CloseConnection":
                log.debug("<sc.protocol.responses.CloseConnection>")
                self.send("</protocol>")
            else:
                log.debug(f"Unknown tag <{tag.tag}>")

    def run_bot(self):
        self.send_move(self.player.get(self.gamestate))

    def join_any_game(self):
        log.info("Joining any game")
        self.send("<join gameType=\"swc_2020_hive\"/>")
        try:
            self.recv()
        except KeyboardInterrupt:
            self.send("<sc.protocol.responses.CloseConnection />")
            self.send("</protocol>")
            self.recv()
        self.socket.close()

    def join_reservation(self, reservation: str):
        log.info("Joining reservation")
        pass
