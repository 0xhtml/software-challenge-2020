import gamestate


class Bot:
    def get(self, gamestate: gamestate.GameState):
        return gamestate.get_possible_set_moves().pop()
