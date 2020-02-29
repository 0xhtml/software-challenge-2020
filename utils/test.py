import _test
from random import choice
import matplotlib.pyplot as plot


class A(_test.players.AlphaBeta):
    pass


class B(_test.players.AlphaBeta):
    def get(self, gamestate: _test.gamestate.GameState):
        return choice(list(gamestate.get_possible_moves()))


count = 32
x = [1, 2]
y = []

for i in x:
    A.max_depth = i
    _, w = _test.test(count, _test.run_local, (A, B))
    y.append(w)

plot.plot(x, y)
plot.show()
