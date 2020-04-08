import _test
from random import choice
from matplotlib import pyplot


class A(_test.players.AlphaBeta):
    def evaluate_single(self, gamestate: _test.gamestate.GameState, color: str):
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
                    value -= self.x * 2
                bee_is_not_set = False

            this_is_dragable = (
                pieces[-1][0] == color and (
                    pieces_len > 1 or
                    gamestate.can_be_disconnected(position)
                )
            )

            if this_is_bee or this_is_dragable:
                for neighbour in _test.players.csocha.neighbours(position):
                    if neighbour in empty:
                        if this_is_dragable:
                            value += 2
                    elif this_is_bee:
                        value -= 20
                        if neighbour in gamestate.board.fields:
                            piece = gamestate.board.fields[neighbour][-1]
                            if piece[1] == "BEETLE":
                                if piece[0] == color:
                                    value += self.x
                                else:
                                    value -= self.x

        if bee_is_not_set:
            value -= 40

        return value


if __name__ == '__main__':
    x = [3, 4, 5]

    data = _test.test(20, x, _test.run_local, (A, _test.players.AlphaBeta))
    pyplot.plot(x, data)
    pyplot.show()
