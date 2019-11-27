from . import gamestate, moves


class Random:
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        possible_moves = gamestate.get_possible_set_moves()
        possible_moves.update(gamestate.get_possible_drag_moves())
        if len(possible_moves) == 0:
            return moves.SkipMove()
        return possible_moves.pop()
