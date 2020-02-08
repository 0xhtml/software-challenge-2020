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

        if (time.clock() - self.now > 1.8):
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
        val = self.evaluate_single(gamestate, gamestate.color)
        val -= self.evaluate_single(gamestate, gamestate.opp)
        return val

    def evaluate_single(self, gamestate: gamestate.GameState, color: str):
        bee = gamestate.bee(color)
        if bee is None:
            val = -10
        else:
            empty = gamestate.board.empty()
            val = -len(gamestate.get_neighbours(bee).difference(empty))
        return val

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.now = time.clock()

        move = self.IDDFS(gamestate)

        print("t", round(time.clock() - self.now, 2))
        return move
