from xml.etree import ElementTree
import csocha

from . import board, moves


class GameState:
    def __init__(self, c: str, t: int, b: board.Board, undep: list):
        self.color = c
        self.opp = "BLUE" if c == "RED" else "RED"
        self.turn = t
        self.board = b
        self.undeployed = undep
        self.directions = [
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, 0),
            (-1, 1),
            (0, 1)
        ]

    def is_connected(self, fields: set) -> bool:
        next = {fields.pop()}
        while len(next) > 0:
            next = {y for x in next for y in csocha.neighbours(x)}
            next.intersection_update(fields)
            fields.difference_update(next)
        return len(fields) == 0

    def get_possible_moves(self) -> set:
        possible_moves = self.get_possible_set_moves()
        possible_moves.update(self.get_possible_drag_moves())
        if len(possible_moves) == 0:
            possible_moves.add(moves.SkipMove())
        return possible_moves

    def get_possible_set_moves(self) -> set:
        # First turn
        if self.turn == 0:
            # All empty fields are possible
            dests = self.board.empty()

        # Second turn
        elif self.turn == 1:
            # Get first set piece
            field = self.board.color(self.opp).__iter__().__next__()

            # Get empty fields
            dests = set(self.board.empty())

            # Only neighbours of piece
            dests.intersection_update(csocha.neighbours(field))

        # All other turns
        else:
            # Get own pieces
            dests = self.board.color(self.color)

            # Get neighbours of own pieces
            dests = {y for x in dests for y in csocha.neighbours(x)}

            # Only empty fields
            dests.intersection_update(self.board.empty())

            # Get opponent pieces
            opp = self.board.color(self.opp)

            # Get neighbours of opponent pieces
            opp = (y for x in opp for y in csocha.neighbours(x))

            # Only fields not next to opponent pieces
            dests.difference_update(opp)

        # When bee isn't set until fith turn player has to set bee
        if (self.turn > 5 and (self.color, "BEE") in self.undeployed):
            types = {"BEE"}
        else:
            types = {x[1] for x in self.undeployed if x[0] == self.color}

        # Return all combinations of pieces and destinations
        return {
            moves.SetMove((self.color, y), x)
            for x in dests
            for y in types
        }

    def get_possible_drag_moves(self) -> set:
        # Drag moves are only possible when bee is set
        if (self.color, "BEE") in self.undeployed:
            return set()

        possible_moves = set()

        # Loop through all set pieces
        for pos in self.board.color(self.color):
            # When there is no piece under piece
            if len(self.board.fields[pos]) == 1:
                # Get all set pieces
                fields = set(self.board.nonempty())

                # Remove piece that is being dragged
                fields.discard(pos)

                # Skip if dragging pieces results in disconnection
                if not self.is_connected(fields):
                    continue

            # Call function to get piece type specific destinations
            if self.board.fields[pos][-1][1] == "BEETLE":
                dests = self.get_beetle_move_dests(pos)
            elif self.board.fields[pos][-1][1] == "BEE":
                dests = self.get_bee_move_dests(pos, pos)
            elif self.board.fields[pos][-1][1] == "SPIDER":
                dests = self.get_spider_move_dests(pos)
            elif self.board.fields[pos][-1][1] == "ANT":
                dests = self.get_ant_move_dests(pos)
            elif self.board.fields[pos][-1][1] == "GRASSHOPPER":
                dests = self.get_grasshopper_move_dests(pos)
            else:
                continue

            # Add all destinations to possible_moves
            possible_moves.update(moves.DragMove(pos, x) for x in dests)

        # Return possible moves
        return possible_moves

    def get_beetle_move_dests(self, pos: tuple) -> set:
        # Get neighbours of pos
        all_neighbours = csocha.neighbours(pos)

        # Only take fields with pieces
        neighbours = set(self.board.nonempty().intersection(all_neighbours))

        # If we are on top of another piece add it aswell
        if len(self.board.fields[pos]) > 1:
            neighbours.add(pos)

        # Get fields next to fields
        dests = {y for x in neighbours for y in csocha.neighbours(x)}

        # Only take fields in reach
        dests.intersection_update(all_neighbours)

        # Only take valid fields
        dests.intersection_update(self.board.fields.keys())

        # Return fields
        return dests

    def get_bee_move_dests(self, pos: tuple, start_pos: tuple) -> set:
        # Get neighbours of pos
        all_neighbours = csocha.neighbours(pos)

        # Only take fields with pieces
        neighbours = set(self.board.nonempty().intersection(all_neighbours))

        # Remove own field
        neighbours.discard(start_pos)

        # Get fields next to fields
        dests = set()
        for neighbour in neighbours:
            dests.symmetric_difference_update(csocha.neighbours(neighbour))

        # Get obstructed fields
        obstructed = self.board.obstructed.copy()

        # Only take obstructed fields in reach
        obstructed.intersection_update(all_neighbours)

        # Get fields next to obscructed fields
        obstructed = (y for x in obstructed for y in csocha.neighbours(x))

        # Remove fields next to obstructed
        dests.difference_update(obstructed)

        # Only take fields in reach
        dests.intersection_update(all_neighbours)

        # Only take empty fields
        dests.intersection_update(self.board.empty())

        # Return fields
        return dests

    def get_spider_move_dests(self, pos: tuple) -> set:
        dests = {pos}
        all_dests = dests.copy()
        for _ in range(3):
            dests = {
                y
                for x in dests
                for y in self.get_bee_move_dests(x, pos)
            }
            dests.difference_update(all_dests)
            all_dests.update(dests)
        return dests

    def get_ant_move_dests(self, pos: tuple) -> set:
        found = set()
        todo = {pos}
        while len(todo) > 0:
            dest = todo.pop()
            found.add(dest)
            dests = self.get_bee_move_dests(dest, pos)
            dests.difference_update(found)
            todo.update(dests)
        found.discard(pos)
        return found

    def get_grasshopper_move_dests(self, pos: tuple) -> set:
        dests = set()
        for direction in self.directions:
            dest = (pos[0] + direction[0], pos[1] + direction[1])
            if dest in self.board.empty():
                continue
            while dest in self.board.nonempty():
                dest = (dest[0] + direction[0], dest[1] + direction[1])
            dests.add(dest)
        dests.intersection_update(self.board.empty())
        return dests

    def bee(self, color: str) -> tuple:
        for field, pieces in self.board.fields.items():
            for piece in pieces:
                if piece == (color, "BEE"):
                    return field
        return None

    def game_ended(self):
        if self.color != "RED":
            return False
        empty = self.board.empty()

        ownbee = self.bee(self.color)
        if ownbee is None:
            own = 0
        else:
            own = len(set(csocha.neighbours(ownbee)).difference(empty))

        oppbee = self.bee(self.opp)
        if oppbee is None:
            opp = 0
        else:
            opp = len(set(csocha.neighbours(oppbee)).difference(empty))

        return own == 6 or opp == 6 or self.turn >= 60

    def __hash__(self, depth=1):
        if self.turn > 7 and self.turn < 60 - depth:
            return csocha.hash(self.board.fields) + str(self.color).encode()
        return csocha.hash(self.board.fields) + str(self.turn).encode()


def parse(xml: ElementTree.Element) -> GameState:
    color = xml.get("currentPlayerColor")
    turn = int(xml.get("turn"))

    _board = board.parse(xml.find("board"))

    undeployed = []
    for piece in xml.findall("*/piece"):
        undeployed.append((piece.get("owner"), piece.get("type")))

    return GameState(color, turn, _board, undeployed)
