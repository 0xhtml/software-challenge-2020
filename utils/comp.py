from _test import create_gamestate
from random import choice
from socha import players, gamestate, moves


class random(players.AlphaBeta):
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        return choice(list(gamestate.get_possible_moves()))


if __name__ == "__main__":
    gamestate = create_gamestate()
    a = players.AlphaBeta()
    b = players.MTDf()
    while not gamestate.game_ended():
        print(a.get(gamestate))
        print(b.get(gamestate))
        print()
        random().get(gamestate).do(gamestate)
