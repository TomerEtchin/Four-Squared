from Player import Player


class HumanPlayer(Player):
    def __init__(self, board, marker):
        Player.__init__(self, board, marker=marker)

    def get_player_move(self):
        """Get move from human player through console input"""
        print(f"Player {self.marker}'s turn")

        # Get part position
        while True:
            try:
                part_input = input("Enter part position (row,col) e.g. '0,1': ")
                row, col = map(int, part_input.split(','))
                part_pos = (row, col)

                if row < 0 or row > 2 or col < 0 or col > 2:
                    print("Invalid position. Row and column must be between 0 and 2.")
                    continue

                if self.board.board[row][col] is None:
                    print("That board position is empty. Choose another position.")
                    continue

                break
            except ValueError:
                print("Invalid input. Please enter as row,col (e.g. '0,1')")

        # Get slot position
        while True:
            try:
                slot_input = input("Enter slot position within part (row,col) e.g. '0,1': ")
                row, col = map(int, slot_input.split(','))
                slot_pos = (row, col)

                if row < 0 or row > 1 or col < 0 or col > 1:
                    print("Invalid position. Row and column must be either 0 or 1.")
                    continue

                # Check if slot is empty
                if self.board.board[part_pos[0]][part_pos[1]].slots[row][col] != 0:
                    print("That slot is already occupied. Choose another slot.")
                    continue

                break
            except ValueError:
                print("Invalid input. Please enter as row,col (e.g. '0,1')")

        # Get target position to move the part
        possible_targets = self.get_possible_targets(part_pos)
        if not possible_targets:
            print("No valid target positions to move this part.")
            return None, None, None

        print("Possible target positions:", possible_targets)

        while True:
            try:
                target_input = input("Enter target position to move part (row,col) e.g. '0,1': ")
                row, col = map(int, target_input.split(','))
                target_pos = (row, col)

                if target_pos not in possible_targets:
                    print("Invalid target position. Choose from:", possible_targets)
                    continue

                break
            except ValueError:
                print("Invalid input. Please enter as row,col (e.g. '0,1')")

        return part_pos, slot_pos, target_pos

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