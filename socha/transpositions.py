class Transpositions:
    _transpositions = {}

    def get(self, gshash: bytes, d: int, turn: int, a: int, b: int) -> tuple:
        if gshash in self._transpositions:
            transposition = self._transpositions[gshash]
            if transposition[0] >= d and (
                (transposition[2] >= b and transposition[1] != 2) or
                (transposition[2] < b and transposition[1] != 1)
            ):
                turn += transposition[3]
                return transposition[2] * (62 - turn), turn
        return None

    def set(self, gshash: bytes, d: int, t: int, v: int, vt: int, ttype: int):
        self._transpositions[gshash] = (d, ttype, int(v / (62 - vt)), vt - t)
