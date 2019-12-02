from . import gamestate, board


class Move:
    pass


class SetMove(Move):
    def __init__(self, piece: tuple, dest: tuple):
        self.piece = piece
        self.dest = dest

    def perform(self, gamestate):
        gamestate.color = "BLUE" if gamestate.color == "RED" else "RED"
        gamestate.turn += 1

        gamestate.undeployed.discard(self.piece)
        gamestate.board.fields[self.dest].append(self.piece)

        return gamestate

    def __xml__(self) -> str:
        z = (-self.dest[0]) + (-self.dest[1])
        return f"""
        <data class="setmove">
        <piece owner="{self.piece[0]}" type="{self.piece[1]}"/>
        <destination x="{self.dest[0]}" y="{self.dest[1]}" z="{z}"/>
        </data>
        """

    def __str__(self) -> str:
        return f"SetMove({self.piece}, {self.dest})"


class DragMove(Move):
    def __init__(self, start: tuple, dest: tuple):
        self.start = start
        self.dest = dest

    def perform(self, gamestate):
        gamestate.color = "BLUE" if gamestate.color == "RED" else "RED"
        gamestate.turn += 1

        piece = gamestate.board.fields[self.start].pop()
        gamestate.board.fields[self.dest].append(piece)

        return gamestate

    def __xml__(self) -> str:
        return f"""
        <data class="dragmove">
        <start x="{self.start.x}" y="{self.start.y}" z="{self.start.z}"/>
        <destination x="{self.dest.x}" y="{self.dest.y}" z="{self.dest.z}"/>
        </data>
        """

    def __str__(self) -> str:
        return f"DragMove({self.start}, {self.dest})"


class SkipMove(Move):
    def perform(self, gamestate):
        gamestate.color = "BLUE" if gamestate.color == "RED" else "RED"
        gamestate.turn += 1
        return gamestate

    def __xml__(self) -> str:
        return "<data class=\"skipmove\"/>"

    def __str__(self) -> str:
        return f"SkipMove()"
