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
        while not self.timeout:
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
        print("d", depth, "e", values[possible_moves[0]], end=" ")
        return possible_moves[0]

    def evaluate(self, gamestate):
        value = (
            -gamestate.pieces_around_bee(gamestate.color)
            + gamestate.pieces_around_bee(gamestate.opp)
        )
        if isinstance(gamestate.last_move, moves.SkipMove):
            value -= 10
        return value

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.now = time.time_ns()

        self.color = gamestate.color
        self.opp = gamestate.opp

        move = self.IDDFS(gamestate)

        then = time.time_ns() - self.now
        print("t", round(then/1000000000, 2))
        return move
