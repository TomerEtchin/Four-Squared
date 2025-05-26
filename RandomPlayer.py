from Player import Player
import random


class RandomPlayer(Player):
    def __init__(self, board, marker):
        Player.__init__(self, board, marker=marker)

    def get_player_move(self):
        print(f"Player {self.marker} (Random) is thinking...")

        # Get all empty slots from the board
        empty_places = self.board.get_empty_places()

        if not empty_places:
            return None, None, None  # No valid moves

        # Get all movable parts positions
        movable_parts = []
        for row in range(3):
            for col in range(3):
                if self.board.board[row][col] is not None:
                    # Check if this part can be moved somewhere
                    if self.get_possible_targets((row, col)):
                        movable_parts.append((row, col))

        if not movable_parts:
            return None, None, None  # No parts can be moved

        # Try to find a valid move (place marker and move different part)
        max_attempts = 30  # Limit attempts to avoid infinite loop
        attempts = 0

        while attempts < max_attempts:
            # Randomly choose a place to put a marker
            part_pos, slot_pos = random.choice(empty_places)

            # Choose a different part to move
            valid_move_parts = [p for p in movable_parts if p != part_pos]

            if not valid_move_parts:
                attempts += 1
                continue  # Try again

            move_part_pos = random.choice(valid_move_parts)

            # Get possible targets for the part to move
            possible_targets = self.get_possible_targets(move_part_pos)

            if possible_targets:
                # Choose a random target position
                target_pos = random.choice(possible_targets)
                return part_pos, slot_pos, move_part_pos

            attempts += 1

        # If we couldn't find a valid move after several attempts
        return None, None, None

    def get_possible_targets(self, part_pos):
        """Get all valid positions where a part can be moved to"""
        targets = []
        row, col = part_pos

        # Check adjacent positions (up, down, left, right)
        possible_adjacents = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for pos in possible_adjacents:
            r, c = pos
            if 0 <= r < 3 and 0 <= c < 3 and self.board.board[r][c] is None:
                targets.append(pos)

        return targets