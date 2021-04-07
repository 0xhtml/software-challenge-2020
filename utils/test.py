import _test
from matplotlib import pyplot


class Player(_test.players.AlphaBeta):
    pass


if __name__ == '__main__':
    x = [3, 4, 5]

    data = _test.test(20, x, _test.run_local, (Player, _test.Random))
    print(data)
    pyplot.plot(x, data)
    pyplot.show()
