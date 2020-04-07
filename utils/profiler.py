import cProfile
import _test
from socha import players

if __name__ == "__main__":
    gamestate = _test.create_gamestate()
    player = players.AlphaBeta()
    player.max_depth = 3
    for _ in range(10):
        player.get(gamestate).do(gamestate)
    cProfile.run("player.get(gamestate)", sort="time")
