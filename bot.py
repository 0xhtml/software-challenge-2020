import field
import gamestate
import move


class Bot:
    def get(self, gamestate: gamestate.GameState):
        t = int(gamestate.turn / 2)
        if not t:
            t = 0
        position = field.Position(-t, 0, t)
        piece = gamestate.get_undeployed(gamestate.color)[0]
        return move.SetMove(piece, position)
