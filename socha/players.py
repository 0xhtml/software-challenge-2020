import math
import time
from . import gamestate, moves

MAX_TIME = 1900000000


class Random:
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        return gamestate.get_possible_moves().pop()


class AlphaBeta:
    transpositions = {}

    def alphaBeta(self, gamestate: gamestate.GameState, depth: int, a, b):
        # boardhash = gamestate.board.hash()
        transposition = None
        # if boardhash in self.transpositions:
        #     transposition = self.transpositions[boardhash]
        #     if (
        #         transposition[0] >= depth and
        #         transposition[1][0] >= a and
        #         transposition[1][1] <= b and
        #         transposition[2] == gamestate.color and
        #         transposition[3] == gamestate.turn
        #     ):
        #         return transposition[4]

        if (time.time_ns() - self.now > MAX_TIME):
            self.timeout = True
        if (depth <= 0 or gamestate.game_ended() or self.timeout):
            return self.evaluate(gamestate)

        if (
            transposition is not None and
            transposition[2] == gamestate.color and
            transposition[3] == gamestate.turn
        ):
            possible_moves = transposition[5]
        else:
            possible_moves = gamestate.get_possible_moves()

        # window = (a, b)
        for move in possible_moves:
            move.do(gamestate)
            value = -self.alphaBeta(
                gamestate,
                depth - 1,
                -b,
                -a
            )
            move.undo(gamestate)
            if value >= b:
                return b
            if value > a:
                a = value

        # if transposition is None:
        #     self.transpositions[boardhash] = (
        #         depth, window, gamestate.color, gamestate.turn, a, possible_moves
        #     )
        return a

    def IDDFS(self, gamestate: gamestate.GameState):
        possible_moves = gamestate.get_possible_moves()
        depth = 0
        values = {}
        self.timeout = False
        while not self.timeout and depth < 20:
            for move in possible_moves:
                move.do(gamestate)
                value = -self.alphaBeta(
                    gamestate,
                    depth,
                    -math.inf,
                    math.inf
                )
                move.undo(gamestate)
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
                    value -= 1000
                else:
                    value += 1000

        return value

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.now = time.time_ns()

        self.color = gamestate.color
        self.opp = gamestate.opp

        move = self.IDDFS(gamestate)

        then = time.time_ns() - self.now
        print("t", round(then/1000000000, 2))
        return move
