import os
import subprocess
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from socha import net


def popen(cmd: str, out) -> subprocess.Popen:
    p = subprocess.Popen(
        cmd.split(),
        cwd="server",
        stdout=out,
        stderr=subprocess.STDOUT
    )
    try:
        p.wait(5)
        raise Exception(cmd + " didn't start")
    except subprocess.TimeoutExpired:
        return p


def test_with_server():
    server = popen("java -jar server.jar", open(os.devnull, "w"))

    try:
        player = popen("java -jar defaultplayer.jar", open(os.devnull, "w"))

        try:
            client = net.Client("localhost", 13050)
            client.join_any_game()
        finally:
            try:
                player.wait(5)
            except subprocess.TimeoutExpired:
                player.terminate()
    finally:
        server.terminate()
