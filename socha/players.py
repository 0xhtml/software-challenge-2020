import math
from . import gamestate, moves


class Random:
    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        return gamestate.get_possible_moves().pop()


class AlphaBeta:
    def __init__(self):
        self.depth = 2
        self.bestMove = None
        self.color = None
        self.opp = None

    def alphaBeta(self, gamestate: gamestate.GameState, depth: int):
        if (depth <= 0): # TODO: or endOfGame
            return self.evaluate(gamestate)
        best = -math.inf
        possible_moves = gamestate.get_possible_moves()
        for move in possible_moves:
            next_gamestate = gamestate.clone()
            next_gamestate = move.perform(next_gamestate)
            value = self.alphaBeta(next_gamestate, depth - 1)
            if value > best:
                if depth == self.depth:
                    self.bestMove = move
                best = value
        return best

    def evaluate(self, gamestate):
        value = (
            -gamestate.pieces_around_bee(self.color)
            +gamestate.pieces_around_bee(self.opp)
        )
        if gamestate.color != self.color:
            return -value
        return value

    def get(self, gamestate: gamestate.GameState) -> moves.Move:
        self.color = gamestate.color
        self.opp = gamestate.opp
        self.alphaBeta(gamestate, self.depth)
        return self.bestMove
