from _test import create_gamestate
from random import choice
from socha import players, gamestate, moves


class random(players.AlphaBeta):
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        return choice(list(gamestate.get_possible_moves()))


if __name__ == "__main__":
    gamestate = create_gamestate()
    a = players.AlphaBeta()
    b = players.MinMax()
    while not gamestate.game_ended():
        print(a.get(gamestate))
        m = b.get(gamestate)
        print(m)
        input()
        m.do(gamestate)
        random().get(gamestate).do(gamestate)
