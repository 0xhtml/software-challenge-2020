import cProfile
import _test

if __name__ == "__main__":
    gamestate = _test.create_gamestate()
    player = _test.players.AlphaBeta()
    for _ in range(5):
        player.get(gamestate).do(gamestate)
        _test.Random().get(gamestate).do(gamestate)
    cProfile.run("player.get(gamestate)", sort="time")
