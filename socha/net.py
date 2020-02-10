import socket
from xml.etree import ElementTree

from . import gamestate, moves, players


class Client:
    def __init__(self, host: str, port: int):
        self.room = None
        self.gamestate = None

        self.player = players.AlphaBeta()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.send("<protocol>")

    def send(self, data: str):
        self.socket.send(data.encode())

    def send_move(self, move: moves.Move):
        print(f"Send move {move}")
        self.send(f"<room roomId=\"{self.room}\">{move.__xml__()}</room>")

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
                    break
                except ElementTree.ParseError:
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
                    self.send_move(self.player.get(self.gamestate))
                elif tagclass == "error":
                    self.send("<sc.protocol.responses.CloseConnection />")
                    self.send("</protocol>")
                    raise Exception(tagdata.get("message"))
                elif tagclass == "result":
                    tagwinner = tagdata.find("winner")
                    if tagwinner is None:
                        print("No body won the game!")
                    else:
                        print(f"{tagwinner.get('color')} won the game!")
                    reason = set()
                    for score in tagdata.findall("score"):
                        reason.add(score.get("reason"))
                    print(*[x + "\n" for x in reason])
                else:
                    print(f"Unknown tag <room class=\"{tagclass}\">")
            elif tag.tag == "left":
                self.send("<sc.protocol.responses.CloseConnection />")
                self.send("</protocol>")
            elif tag.tag == "sc.protocol.responses.CloseConnection":
                self.send("</protocol>")
            else:
                print(f"Unknown tag <{tag.tag}>")

    def run(self):
        try:
            self.recv()
        except KeyboardInterrupt:
            self.send("<sc.protocol.responses.CloseConnection />")
            self.send("</protocol>")
            self.recv()
        finally:
            self.socket.close()

    def join_any_game(self):
        self.send("<join gameType=\"swc_2020_hive\"/>")
        self.run()

    def join_reservation(self, reservation: str):
        self.send(f"<joinPrepared reservationCode=\"{reservation}\" />")
        self.run()
