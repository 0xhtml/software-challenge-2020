import _test
from random import choice
from multiprocessing import Pool
from matplotlib import pyplot


class A(_test.players.AlphaBeta):
    def get(self, gamestate: _test.gamestate.GameState):
        self.max_depth = self.x
        return super().get(gamestate)


class B(_test.players.AlphaBeta):
    def get(self, gamestate: _test.gamestate.GameState):
        return choice(list(gamestate.get_possible_moves()))


def run(x):
    return _test.test(30, _test.run_local, (A, B, x))


if __name__ == '__main__':
    pool = Pool(3)

    x = [1, 2, 3]

    pyplot.plot(x, pool.map(run, x))
    pyplot.show()

    pool.close()
