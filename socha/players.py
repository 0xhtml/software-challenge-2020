import math
import time
from . import gamestate, moves


class AlphaBeta:
    sort_table = {}

    def alphaBeta(self, gs: gamestate.GameState, depth: int, a: int, b: int):
        # Check for timeout
        if (time.clock() - self.now > 1.8):
            self.timeout = True

        # If depth reached, end of game or timeout reached then stop
        if (depth <= 0 or gs.game_ended() or self.timeout):
            return self.evaluate(gs)

        # Go through all moves
        possible_moves = sorted(
            gs.get_possible_moves(),
            key=lambda x: self.sort_table.get(hash(x), -math.inf),
            reverse=True
        )
        for move in possible_moves:
            # Do move
            move.do(gs)

            value = -self.alphaBeta(gs, depth - 1, -b, -a)
            self.sort_table[move.__hash__()] = value

            # Undo move
            move.undo(gs)

            # Beta-cutoff
            if value >= b:
                return b

            # New best move
            if value > a:
                a = value

        # Return value
        return a

    def IDDFS(self, gamestate: gamestate.GameState):
        # Reset timeout
        self.timeout = False

        # Set initial values
        depth = 0
        values = {}

        # Get all possible moves
        possible_moves = list(gamestate.get_possible_moves())

        # Do pvSearch while not timed out and depth under 20
        while not self.timeout and depth < 3:
            # Go through all moves
            for move in possible_moves:
                # Do move
                move.do(gamestate)

                # Perform pvSearch
                value = -self.alphaBeta(
                    gamestate,
                    depth,
                    -math.inf,
                    math.inf
                )

                # Undo move
                move.undo(gamestate)

                self.sort_table[move.__hash__()] = value

                # Test if timeout was reached making value invalid
                if self.timeout:
                    break

                # Save value for next iteration and result
                values[move] = value

            # Sort moves based on values
            possible_moves = sorted(
                possible_moves,
                key=lambda m: values.get(m, -math.inf),
                reverse=True
            )

            # Increase depth for next iteration
            depth += 1

        # Log info
        print("d", depth, "e", values.get(possible_moves[0]), end=" ")

        # Return best move
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
