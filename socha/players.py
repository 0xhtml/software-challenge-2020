import math
import time
from . import gamestate, moves


class AlphaBeta:
    transpositions = {}

    def alphaBeta(self, gamestate: gamestate.GameState, depth: int, a, b):
        boardhash = hash(gamestate.board)
        if boardhash in self.transpositions:
            transposition = self.transpositions[boardhash]
            if (
                transposition[0] >= depth and
                transposition[1][0] >= a and
                transposition[1][1] <= b and
                transposition[2] == gamestate.color and
                (
                    (
                        gamestate.turn > 5 and
                        gamestate.turn + transposition[0] < 60
                    ) or transposition[3] == gamestate.turn
                )
            ):
                return transposition[4]

        if (time.time_ns() - self.now > 1900000000):
            self.timeout = True
        if (depth <= 0 or gamestate.game_ended() or self.timeout):
            return self.evaluate(gamestate)

        window = (a, b)
        for move in gamestate.get_possible_moves():
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

        self.transpositions[boardhash] = (
            depth, window, gamestate.color, gamestate.turn, a
        )
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
        empty = gamestate.board.empty()
        own = len(gamestate.around_bee(gamestate.color).difference(empty))
        opp = len(gamestate.around_bee(gamestate.opp).difference(empty))
        return (opp or 10) - (own or 10)

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.now = time.time_ns()

        move = self.IDDFS(gamestate)

        then = time.time_ns() - self.now
        print("t", round(then/1000000000, 2))
        return move
