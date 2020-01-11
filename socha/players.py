import math
import time
from . import gamestate, moves


class Random:
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        return gamestate.get_possible_moves().pop()


class AlphaBeta:
    MAX_TIME = 1900000000

    def alphaBeta(self, gamestate: gamestate.GameState, depth: int, a, b):
        if (time.time_ns() - self.now > self.MAX_TIME):
            self.timeout = True
        if (depth <= 0 or gamestate.game_ended() or self.timeout):
            return self.evaluate(gamestate)
        possible_moves = gamestate.get_possible_moves()
        for move in possible_moves:
            value = -self.alphaBeta(
                move.perform(gamestate.clone()),
                depth - 1,
                -b,
                -a
            )
            if value >= b:
                return b
            if value > a:
                a = value
        return a

    def IDDFS(self, gamestate: gamestate.GameState):
        possible_moves = gamestate.get_possible_moves()
        depth = 0
        values = {}
        self.timeout = False
        while not self.timeout and depth < 20:
            for move in possible_moves:
                value = self.alphaBeta(
                    move.perform(gamestate.clone()),
                    depth,
                    -math.inf,
                    math.inf
                )
                if self.timeout:
                    break
                values[move] = value
            possible_moves = sorted(
                possible_moves,
                key=lambda m: values.get(m, -math.inf),
                reverse=True
            )
            depth += 1
        print("d", depth, "e", values.get(possible_moves[0]), end=" ")
        return possible_moves[0]

    def evaluate(self, gamestate: gamestate.GameState):
        own = gamestate.around_bee(gamestate.color)
        opp = gamestate.around_bee(gamestate.opp)
        empty = gamestate.board.empty()

        value = (
            (len(opp.difference(empty)) or 10)
            - (len(own.difference(empty)) or 10)
        )

        if len(own.difference(empty)) == 6:
            value -= 200
        if len(opp.difference(empty)) == 6:
            value += 200

        for i, move in enumerate(reversed(gamestate.moves)):
            if isinstance(move, moves.SkipMove):
                if i % 2 == 0:
                    value += 1000
                else:
                    value -= 1000

        return -value

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.now = time.time_ns()

        self.color = gamestate.color
        self.opp = gamestate.opp

        move = self.IDDFS(gamestate)

        then = time.time_ns() - self.now
        print("t", round(then/1000000000, 2))
        return move
