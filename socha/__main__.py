import sys

from . import net


def run(host="localhost", port=13050, reservation=None):
    client = net.Client(host, port)

    if reservation is None:
        client.join_any_game()
    else:
        client.join_reservation(reservation)


if __name__ == "__main__":
    run(*sys.argv[1:])
