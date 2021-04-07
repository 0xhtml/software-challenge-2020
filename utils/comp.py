import test
import _test

if __name__ == "__main__":
    gamestate = _test.create_gamestate()
    a = _test.players.AlphaBeta()
    b = test.Player()
    while not gamestate.game_ended():
        print(a.get(gamestate))
        m = b.get(gamestate)
        print(m)
        input()
        m.do(gamestate)
