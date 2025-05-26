import numpy as np

class boardPart:
    def __init__(self):
        self.slots = [
            [0, 0],
            [0, 0]
        ] # 0 - Empty, 1 - Blue, 2 - Red

    def is_full(self):
        for row in range(2):
            for col in range(2):
                if self.slots[row][col] == 0:
                    return False
        return True


class Board:
    def __init__(self):
        self.board = [
            [boardPart(), boardPart(), boardPart()],
            [boardPart() ,None, boardPart() ],
            [boardPart(), boardPart(), boardPart()]
        ]

    def print_board(self):
        for row in self.board:
            if None not in row:
                print(f"{row[0].slots[0][0]} {row[0].slots[0][1]} {row[1].slots[0][0]} {row[1].slots[0][1]} {row[2].slots[0][0]} {row[2].slots[0][1]}")
                print(f"{row[0].slots[1][0]} {row[0].slots[1][1]} {row[1].slots[1][0]} {row[1].slots[1][1]} {row[2].slots[1][0]} {row[2].slots[1][1]}")
            else:
                # Print first row
                for part in row:
                    if part == None:
                        print("    ", end="")
                    else:
                       print(f"{part.slots[0][0]} {part.slots[0][1]} ", end="")
                print()

                # Print second row
                for part in row:
                    if part == None:
                        print("    ", end="")
                    else:
                        print(f"{part.slots[1][0]} {part.slots[1][1]} ", end="")
                print()



    def can_part_move (self, pos, new_pos): # move (row, col) dir (row, col)
        row_pos, col_pos = pos
        row_new, col_new = new_pos

        if row_pos < 0 or row_pos > 2 or col_pos < 0 or col_pos > 2:
            print("Move invalid")
            return False

        if row_new < 0 or row_new > 2 or col_new < 0 or col_new > 2:
            print("Move invalid")
            return False

        if (row_pos == row_new and abs(col_pos - col_new) == 1):
            return True

        if (col_pos == col_new and abs(row_pos - row_new) == 1):
            return True

        return False

    def place_marker(self, part_pos, slot_pos, player): #first part of submit move
        """part_pos: (row, col) of the board part to play on
slot_pos: (row, col) of the slot within the part
target_pos: (row, col) of where to move the part after playing
player: 1 for Blue, 2 for Red"""
        row_part, col_part = part_pos
        row_slot, col_slot = slot_pos

        # Check if part exists
        if self.board[row_part][col_part] is None:
            print("Part is None")
            return False

        # Get the board part
        part = self.board[row_part][col_part]

        # Check if slot is empty
        if part.slots[row_slot][col_slot] != 0:
            print("Slot is occupied")
            return False

        # Make the move
        part.slots[row_slot][col_slot] = player
        return True  # Return True for successful placement

    def move_part(self, part_pos, target_pos):  # part 2 of submit move
        row_part, col_part = part_pos
        row_target, col_target = target_pos

        # Check if part exists
        if self.board[row_part][col_part] is None:
            print("Part is None")
            return False

        # Check if target position is empty
        if self.board[row_target][col_target] is not None:
            print("Target position is not empty")
            return False

        # Check if part can move to target position
        if not self.can_part_move(part_pos, target_pos):
            print(f"Part cannot move from {part_pos} to {target_pos}")
            return False

        # Move the part
        self.board[row_target][col_target] = self.board[row_part][col_part]
        self.board[row_part][col_part] = None
        return True



    def is_winner(self, player):
        """
                Check if player has won by having 4 markers in a square pattern.
                This can happen in two ways:
                1. A single BoardPart is completely filled with the player's markers
                2. Adjacent BoardParts form a 2x2 square of the player's markers
                """
        # Check if any BoardPart is completely filled with player's markers
        for row in range(3):
            for col in range(3):
                part = self.board[row][col]
                if part is not None:
                    if (part.slots[0][0] == player and
                            part.slots[0][1] == player and
                            part.slots[1][0] == player and
                            part.slots[1][1] == player):
                        return True

        # Check for 2x2 squares across adjacent BoardParts
        # We need to check the edges between parts

        # Check horizontal adjacency (right side of one part, left side of adjacent part)
        for row in range(3):
            for col in range(2):  # Only check columns 0 and 1 since we need column+1
                left_part = self.board[row][col]
                right_part = self.board[row][col + 1]

                if left_part is not None and right_part is not None:
                    # Check top edge
                    if (left_part.slots[0][1] == player and  # Top-right of left part
                            right_part.slots[0][0] == player and  # Top-left of right part
                            left_part.slots[1][1] == player and  # Bottom-right of left part
                            right_part.slots[1][0] == player):  # Bottom-left of right part
                        return True

        # Check vertical adjacency (bottom side of one part, top side of part below)
        for row in range(2):  # Only check rows 0 and 1 since we need row+1
            for col in range(3):
                top_part = self.board[row][col]
                bottom_part = self.board[row + 1][col]

                if top_part is not None and bottom_part is not None:
                    # Check left edge
                    if (top_part.slots[1][0] == player and  # Bottom-left of top part
                            bottom_part.slots[0][0] == player and  # Top-left of bottom part
                            top_part.slots[1][1] == player and  # Bottom-right of top part
                            bottom_part.slots[0][1] == player):  # Top-right of bottom part
                        return True

        # Check diagonal adjacency (corner of 4 different parts)
        for row in range(2):
            for col in range(2):
                top_left = self.board[row][col]
                top_right = self.board[row][col + 1]
                bottom_left = self.board[row + 1][col]
                bottom_right = self.board[row + 1][col + 1]

                if (top_left is not None and top_right is not None and
                        bottom_left is not None and bottom_right is not None):
                    if (top_left.slots[1][1] == player and  # Bottom-right of top-left part
                            top_right.slots[1][0] == player and  # Bottom-left of top-right part
                            bottom_left.slots[0][1] == player and  # Top-right of bottom-left part
                            bottom_right.slots[0][0] == player):  # Top-left of bottom-right part
                        return True

        return False

    def is_full(self):
        for row in range(3):
            for col in range(3):
                part = self.board[row][col]
                # Skip the None in the middle
                if part is None:
                    continue
                # Check if any slot in this BoardPart is empty
                for slot_row in range(2):
                    for slot_col in range(2):
                        if part.slots[slot_row][slot_col] == 0:
                            return False
        return True

    def is_tie(self):
        if self.is_full() and not self.is_winner(2) and not self.is_winner(1):
            return True
        return False

    def get_empty_places(self):
        """
        Returns a list of empty slots as tuples: ((board_row, board_col), (slot_row, slot_col))
        Each tuple represents a position where a player can place their marker.
        """
        empty_places = []
        for board_row in range(3):
            for board_col in range(3):
                part = self.board[board_row][board_col]
                # Skip the None in the middle
                if part is None:
                    continue
                # Check each slot in this BoardPart
                for slot_row in range(2):
                    for slot_col in range(2):
                        if part.slots[slot_row][slot_col] == 0:
                            empty_places.append(((board_row, board_col), (slot_row, slot_col)))
        return empty_places

    def get_str_board(self):
        """
        Returns a string representation of the complete board.
        """
        str_board = ""

        # Loop through each row of BoardParts
        for board_row in range(3):
            # First row of slots in each BoardPart
            for slot_row in range(2):
                for board_col in range(3):
                    part = self.board[board_row][board_col]
                    if part is None:
                        str_board += "  "  # Two spaces for None
                    else:
                        for slot_col in range(2):
                            # Convert integers to characters for readability
                            value = part.slots[slot_row][slot_col]
                            if value == 0:
                                str_board += "."
                            elif value == 1:
                                str_board += "B"  # Blue
                            elif value == 2:
                                str_board += "R"  # Red
                            else:
                                str_board += str(value)

                            # Add space between slots except at the end of a row
                            if slot_col < 1 or board_col < 2:
                                str_board += " "

                # New line after each row of slots
                str_board += "\n"

        return str_board

    def str_board_history(self):
        """
        Returns a compact string representation of the board without newlines,
        suitable for storing in game history.
        """
        history_str = ""

        # Loop through each row of BoardParts
        for board_row in range(3):
            for board_col in range(3):
                part = self.board[board_row][board_col]
                if part is None:
                    history_str += "XX"  # Use XX to represent the None spot
                else:
                    for slot_row in range(2):
                        for slot_col in range(2):
                            value = part.slots[slot_row][slot_col]
                            history_str += str(value)

        return history_str
