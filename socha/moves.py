from . import pos


class Move:
    pass


class SetMove(Move):
    def __init__(self, piece: tuple, dest: pos.Pos):
        self.piece = piece
        self.dest = dest

    def __xml__(self) -> str:
        return f"""
        <data class="setmove">
        <piece owner="{self.piece[0]}" type="{self.piece[1]}"/>
        <destination x="{self.dest.x}" y="{self.dest.y}" z="{self.dest.z}"/>
        </data>
        """

    def __str__(self) -> str:
        return f"SetMove({self.piece}, {self.dest})"


class DragMove(Move):
    def __init__(self, start: pos.Pos, dest: pos.Pos):
        self.start = start
        self.dest = dest

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
    def __xml__(self) -> str:
        return "<data class=\"skipmove\"/>"

    def __str__(self) -> str:
        return f"SkipMove()"
