import _test
from random import choice
from matplotlib import pyplot


class A(_test.players.AlphaBeta):
    def get(self, gamestate: _test.gamestate.GameState):
        self.max_depth = self.x
        return super().get(gamestate)


class B(_test.players.AlphaBeta):
    def get(self, gamestate: _test.gamestate.GameState):
        return choice(list(gamestate.get_possible_moves()))


if __name__ == '__main__':
    x = [0, 7, 8, 9, 10, 11, 12, 13, 14]

    data = _test.test(40, x, _test.run_server, (A,))
    pyplot.plot(x, data)
    pyplot.show()
