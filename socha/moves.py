class Move:
    def do(self, gamestate):
        color, opponent = gamestate.color, gamestate.opponent
        gamestate.color, gamestate.opponent = opponent, color
        gamestate.turn += 1
        gamestate.board.cache = {}

    def undo(self, gamestate):
        color, opponent = gamestate.color, gamestate.opponent
        gamestate.color, gamestate.opponent = opponent, color
        gamestate.turn -= 1
        gamestate.board.cache = {}


class SetMove(Move):
    def __init__(self, piece: tuple, dest: tuple):
        self.piece = piece
        self.dest = dest

    def do(self, gamestate):
        gamestate.undeployed.remove(self.piece)
        gamestate.board.fields[self.dest].append(self.piece)
        super().do(gamestate)

    def undo(self, gamestate):
        gamestate.undeployed.append(self.piece)
        gamestate.board.fields[self.dest].pop()
        super().undo(gamestate)

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

    def hash(self, _fields) -> str:
        return f"{self.piece[1]}_{self.dest[0]}_{self.dest[1]}"


class DragMove(Move):
    def __init__(self, start: tuple, dest: tuple):
        self.start = start
        self.dest = dest

    def do(self, gamestate):
        piece = gamestate.board.fields[self.start].pop()
        gamestate.board.fields[self.dest].append(piece)
        super().do(gamestate)

    def undo(self, gamestate):
        piece = gamestate.board.fields[self.dest].pop()
        gamestate.board.fields[self.start].append(piece)
        super().undo(gamestate)

    def __xml__(self) -> str:
        start_z = (-self.start[0]) + (-self.start[1])
        dest_z = (-self.dest[0]) + (-self.dest[1])
        return f"""
        <data class="dragmove">
        <start x="{self.start[0]}" y="{self.start[1]}" z="{start_z}"/>
        <destination x="{self.dest[0]}" y="{self.dest[1]}" z="{dest_z}"/>
        </data>
        """

    def __str__(self) -> str:
        return f"DragMove({self.start}, {self.dest})"

    def hash(self, fields: dict) -> str:
        return f"{fields[self.start][-1][1]}_{self.dest[0]}_{self.dest[1]}"


class SkipMove(Move):
    def __xml__(self) -> str:
        return "<data class=\"skipmove\"/>"

    def __str__(self) -> str:
        return "SkipMove()"

    def hash(self, _fields) -> str:
        return "S"
