import math
import time
from . import gamestate, moves


class Random:
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        return gamestate.get_possible_moves().pop()


class AlphaBeta:
    def __init__(self):
        self.depth = 2
        self.best = (None, None)
        self.color = None
        self.opp = None

    def alphaBeta(self, gamestate: gamestate.GameState, depth: int, a, b):
        if (depth <= 0):  # TODO: or endOfGame
            return self.evaluate(gamestate)
        best = -math.inf
        possible_moves = gamestate.get_possible_moves()
        for move in possible_moves:
            next_gamestate = gamestate.clone()
            next_gamestate = move.perform(next_gamestate)
            value = -self.alphaBeta(next_gamestate, depth - 1, -b, -a)
            if value > best:
                if value >= b:
                    return value
                best = value
                if depth == self.depth:
                    self.best = (value, move)
                if value > a:
                    a = value
        return best

    def evaluate(self, gamestate):
        value = (
            -gamestate.pieces_around_bee(self.color)
            + gamestate.pieces_around_bee(self.opp)
        )
        if gamestate.color != self.color:
            return -value
        return value

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        now = time.time_ns()
        self.color = gamestate.color
        self.opp = gamestate.opp
        self.alphaBeta(gamestate, self.depth, -math.inf, math.inf)
        then = time.time_ns() - now
        print(f"Time: {round(then/1000000000, 2)} s")
        print(f"Eval: {self.best[0]}")
        return self.best[1]
