import math
import time
import csocha
from . import gamestate, moves


class AlphaBeta:
    transpositions = {}
    max_depth = 5

    def alpha_beta(self, gs: gamestate.GameState, depth: int, a: int, b: int):
        # Check for timeout
        if (time.time_ns() - self.now > 1900000000):
            self.timeout = True
            return 0

        # Generate gamestate hash
        gshash = gs.hash(depth)

        # Check for transposition
        if gshash in self.transpositions:
            # Get transposition
            transposition = self.transpositions[gshash]

            # Check transposition depth
            if transposition[0] >= depth:
                if transposition[1] == 0:
                    # Exact
                    return transposition[2]
                if transposition[1] == 1:
                    # Upper bound
                    b = min(transposition[2], b)
                if transposition[1] == 2:
                    # Lower bound
                    a = max(transposition[2], a)

                # Cut off
                if a > b:
                    return a

        # If depth reached or end of game then stop
        if (depth <= 0 or gs.game_ended()):
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

            value = -self.alpha_beta(gs, depth - 1, -b, -a)

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
            self.transpositions[gshash] = (depth, 1, a)
        elif a > b:
            # Insert into transposition table as lower bound
            self.transpositions[gshash] = (depth, 2, a)
        else:
            # Insert into transposition table as exact
            self.transpositions[gshash] = (depth, 0, a)

        # Return value
        return a

    def iddfs(self, gamestate: gamestate.GameState):
        # Reset timeout and history
        self.timeout = False
        self.history = {}

        # Set initial values
        depth = 0
        values = {}

        # Get all possible moves
        possible_moves = list(gamestate.get_possible_moves())

        # Do AlphaBeta while not timed out and depth under max depth
        while not self.timeout and depth < self.max_depth:
            # Go through all moves
            for move in possible_moves:
                # Do move
                move.do(gamestate)

                # Perform AlphaBeta
                value = -self.alpha_beta(gamestate, depth, -math.inf, math.inf)

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
        print(*[
            "{:3d} {}".format(values.get(m), str(m))
            for m in possible_moves
        ], sep="\n")
        print("d", depth, "e", values.get(possible_moves[0]), end=" ")

        # Return best move
        return possible_moves[0]

    def evaluate(self, gamestate: gamestate.GameState):
        val = self.evaluate_single(gamestate, gamestate.color)
        val -= self.evaluate_single(gamestate, gamestate.opponent)
        return val

    def evaluate_single(self, gamestate: gamestate.GameState, color: str):
        empty = gamestate.board.empty()
        bee = (color, "BEE")

        value = 0

        bee_is_not_set = True
        for position, pieces in gamestate.board.fields.items():
            pieces_len = len(pieces)

            if pieces_len == 0:
                continue

            this_is_bee = bee_is_not_set and pieces[0] == bee
            if this_is_bee:
                if pieces[-1][1] == "BEETLE" and pieces[-1][0] != color:
                    value -= 4
                bee_is_not_set = False

            this_is_dragable = (
                pieces[-1][0] == color and (
                    pieces_len > 1 or
                    gamestate.can_be_disconnected(position)
                )
            )

            if this_is_bee or this_is_dragable:
                for neighbour in csocha.neighbours(position):
                    if neighbour in empty:
                        if this_is_dragable:
                            value += 1
                    elif this_is_bee:
                        value -= 11
                        if neighbour in gamestate.board.fields:
                            piece = gamestate.board.fields[neighbour][-1]
                            if piece[1] == "BEETLE":
                                if piece[0] == color:
                                    value += 2
                                else:
                                    value -= 2

        if bee_is_not_set:
            value -= 22

        return value

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.now = time.time_ns()

        move = self.iddfs(gamestate)

        print("t", round((time.time_ns() - self.now) / 1000000000, 2))
        return move
