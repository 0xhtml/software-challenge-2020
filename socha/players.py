import math
import time
from . import gamestate, moves


class Random:
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        return gamestate.get_possible_moves().pop()


class AlphaBeta:
    MAX_TIME = 1900000000

    def alphaBeta(self, gamestate: gamestate.GameState, depth: int, a, b):
        if (depth <= 0 or time.time_ns() - self.now > self.MAX_TIME):
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
                    self.best[depth] = (value, move)
                if value > a:
                    a = value
        return best

    def IDDFS(self, gamestate: gamestate.GameState):
        self.depth = 0
        while time.time_ns() - self.now < self.MAX_TIME:
            self.depth += 1
            self.alphaBeta(gamestate, self.depth, -math.inf, math.inf)
        if self.best[self.depth][0] > self.best[self.depth-1][0]:
            print(f"Depth: {self.depth}")
            return self.best[self.depth]
        print(f"Depth: {self.depth-1}")
        return self.best[self.depth-1]

    def evaluate(self, gamestate):
        value = (
            -gamestate.pieces_around_bee(self.color)
            + gamestate.pieces_around_bee(self.opp)
        )
        if gamestate.color != self.color:
            return -value
        return value

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.now = time.time_ns()

        self.best = {}
        self.color = gamestate.color
        self.opp = gamestate.opp

        move = self.IDDFS(gamestate)

        then = time.time_ns() - self.now
        print(f"Time: {round(then/1000000000, 2)} s")
        print(f"Eval: {move[0]}")
        return move[1]
