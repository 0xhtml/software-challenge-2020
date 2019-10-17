class Move:
    def __init__(self):
        raise NotImplementedError

    def to_xml(self):
        raise NotImplementedError


class SetMove(Move):
    def __init__(self, piece: tuple, pos: tuple):
        self.piece = piece
        self.pos = pos

    def to_xml(self) -> str:
        return f"""
        <data class="setmove">
        <piece owner="{self.piece[0]}" type="{self.piece[1]}"/>
        <destination x="{self.pos[0]}" y="{self.pos[1]}" z="{self.pos[2]}"/>
        </data>
        """

    def __str__(self) -> str:
        return f"SetMove({self.piece}, {self.pos})"


class DragMove(Move):
    def __init__(self, start: tuple, dest: tuple):
        self.start = start
        self.dest = dest

    def to_xml(self) -> str:
        return f"""
        <data class="dragmove">
        <start x="{self.start[0]}" y="{self.start[1]}" z="{self.start[2]}"/>
        <destination x="{self.dest[0]}" y="{self.dest[1]}" z="{self.dest[2]}"/>
        </data>
        """

    def __str__(self) -> str:
        return f"DragMove({self.start}, {self.dest})"


class MissMove(Move):
    def __init__(self):
        pass

    def to_xml(self) -> str:
        return "<data class=\"missmove\"/>"

    def __str__(self) -> str:
        return f"MissMove()"
