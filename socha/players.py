import math
import time
import csocha
from . import gamestate, moves


class AlphaBeta:
    tranpositions = {}
    history = {}

    def alphaBeta(self, gs: gamestate.GameState, depth: int, a: int, b: int):
        # Generate gamestate hash
        gshash = gs.hash(depth)

        # Check for transposition
        if gshash in self.tranpositions:
            # Get transposition
            transposition = self.tranpositions[gshash]

            # Check transposition depth
            if transposition[0] >= depth:
                if transposition[1] == 0:
                    # Exact
                    return transposition[2]
                elif transposition[1] == 1:
                    # Upper bound
                    b = min(transposition[2], b)
                elif transposition[1] == 2:
                    # Lower bound
                    a = max(transposition[2], a)

                # Cut off
                if a > b:
                    return a

        # Check for timeout
        if (time.clock() - self.now > 1.8):
            self.timeout = True

        # If depth reached, end of game or timeout reached then stop
        if (depth <= 0 or gs.game_ended() or self.timeout):
            return self.evaluate(gs)

        # Save alpha for later use
        start_a = a

        # Get possible moves sorted based on history
        possible_moves = sorted(
            gs.get_possible_moves(),
            key=lambda x: self.history.get(x.hash(gs.board.fields), 0),
            reverse=True
        )

        # Go through all moves
        for move in possible_moves:
            # Do move
            move.do(gs)

            value = -self.alphaBeta(gs, depth - 1, -b, -a)

            # Undo move
            move.undo(gs)

            # New best alpha
            if value > a:
                a = value

            # Beta-cutoff
            if value >= b:
                mhash = move.hash(gs.board.fields)
                self.history[mhash] = self.history.get(mhash, 0) + (depth ** 2)
                break

        if a <= start_a:
            # Insert into transposition table as upper bound
            self.tranpositions[gshash] = (depth, 1, a)
        elif a > b:
            # Insert into transposition table as lower bound
            self.tranpositions[gshash] = (depth, 2, a)
        else:
            # Insert into transposition table as exact
            self.tranpositions[gshash] = (depth, 0, a)

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
            return 0
        empty = gamestate.board.empty()
        return -len(set(csocha.neighbours(bee)).difference(empty))

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.now = time.clock()

        move = self.IDDFS(gamestate)

        print("t", round(time.clock() - self.now, 2))
        return move
