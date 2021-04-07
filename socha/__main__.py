import argparse
from . import net

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", default="localhost")
    parser.add_argument("-p", type=int, default=13050)
    parser.add_argument("-r", default=None)
    args = parser.parse_args()

    client = net.Client(args.h, args.p)

    if args.r is None:
        client.join_any_game()
    else:
        client.join_reservation(args.r)
