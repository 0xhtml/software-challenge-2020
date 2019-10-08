import piece
import field


class Move:
    def __init__(self):
        raise Exception("Unimplemented")

    def to_xml(self):
        raise Exception("Unimplemented")


class SetMove(Move):
    def __init__(self, piece: piece.Piece, pos: field.Position):
        self.piece = piece
        self.pos = pos

    def to_xml(self):
        return f"""
        <data class="setmove">
            <piece owner="{self.piece.color}" type="{self.piece.type}"/>
            <destination x="{self.pos.x}" y="{self.pos.y}" z="{self.pos.z}"/>
        </data>
        """


class DragMove(Move):
    def __init__(self, start: field.Position, dest: field.Position):
        self.start = start
        self.dest = dest

    def to_xml(self):
        return f"""
        <data class="dragmove">
            <start x="{self.start.x}" y="{self.start.y}" z="{self.start.z}"/>
            <destination x="{self.dest.x}" y="{self.dest.y}" z="{self.dest.z}"/>
        </data>
        """


class MissMove(Move):
    def to_xml(self):
        return "<data class=\"missmove\"/>"
