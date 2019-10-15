import subprocess
import time
from socha import net
import os


def test_with_server():
    server = subprocess.Popen(["java", "-jar", "server.jar"], cwd="server", stdout=open("s.log", "w"), stderr=subprocess.STDOUT)
    time.sleep(5)

    player = subprocess.Popen(["java", "-jar", "defaultplayer.jar"], cwd="server", stdout=open("p.log", "w"), stderr=subprocess.STDOUT)
    time.sleep(5)

    client = net.Client("localhost", 13050)
    client.join_any_game()

    player.wait()
    server.terminate()
    server.wait()
