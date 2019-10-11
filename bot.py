import gamestate
import move


class Bot:
    def get(self, gamestate: gamestate.GameState):
        possible_moves = gamestate.get_possible_set_moves()
        if len(possible_moves) == 0:
            return move.MissMove()
        return possible_moves.pop()
