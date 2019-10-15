import subprocess
import time
from socha import net
import os


def test_with_server():
    server = subprocess.Popen(["java", "-jar", "server.jar"], cwd="server", stdout=open("s.log", "w"), stderr=subprocess.STDOUT)
    time.sleep(5)

    try:
        for _ in range(2):
            player = subprocess.Popen(["java", "-jar", "defaultplayer.jar"], cwd="server", stdout=open("p.log", "w"), stderr=subprocess.STDOUT)
            time.sleep(5)

            try:
                client = net.Client("localhost", 13050)
                client.join_any_game()
            finally:
                try:
                    player.wait(5)
                except subprocess.TimeoutExpired:
                    player.terminate()
                    player.wait()
    finally:
        server.terminate()
        server.wait()
