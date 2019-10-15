import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from socha import __main__


class DummyClient:
    def __init__(self, host, port):
        assert host == "host"
        assert port == 1234

    def join_any_game(self):
        pass

    def join_reservation(self, reservation):
        assert reservation == "reservation"


def test_cli():
    __main__.net.Client = DummyClient
    __main__.run("host", "1234")
    __main__.run("host", "1234", "reservation")
