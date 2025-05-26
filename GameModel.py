from Board import Board
from SmartAgent import SmartAgent
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from AIAgent import AiAgent
import json
import os


class GameModel:
    def __init__(self):
        self.board = Board()
        self.player1 = None  # Blue player (1)
        self.player2 = None  # Red player (2)
        self.player1_type = 1  # Default: Human
        self.player2_type = 1  # Default: Human
        self.current_player = 1  # Blue starts
        self.game_history = []
        self.gamma = 0.9  # Default value for learning rate
        self.winner = None
        self.load_game_stats()
        self.stats = {"blue_wins": 0, "red_wins": 0, "draws": 0}

    def setup_players(self, player1_type, player2_type):
        """Setup players based on selected types
        Types: 1 - Human, 2 - Random, 3 - Smart"""
        self.player1_type = player1_type
        self.player2_type = player2_type

        # Player 1 (Blue)
        if player1_type == 1:
            self.player1 = HumanPlayer(self.board, 1)
        elif player1_type == 2:
            self.player1 = RandomPlayer(self.board, 1)
        elif player1_type == 3:
            self.player1 = SmartAgent(self.board, 1)
        elif player1_type == 4:
            self.player1 = AiAgent(self.board, 1)

        # Player 2 (Red)
        if player2_type == 1:
            self.player2 = HumanPlayer(self.board, 2)
        elif player2_type == 2:
            self.player2 = RandomPlayer(self.board, 2)
        elif player2_type == 3:
            self.player2 = SmartAgent(self.board, 2)
        elif player2_type == 4:
            self.player2 = AiAgent(self.board, 2)

    def reset_game(self):
        """Reset the game board and state"""
        self.board = Board()
        self.current_player = 1  # Blue starts
        self.game_history = []
        self.winner = None

    def get_current_player_object(self):
        """Get the current player object"""
        return self.player1 if self.current_player == 1 else self.player2

    def get_current_player_type(self):
        """Get the current player type"""
        return self.player1_type if self.current_player == 1 else self.player2_type

    def switch_player(self):
        """Switch to the next player (should always be 1 or 2)."""
        self.current_player = 2 if self.current_player == 1 else 1

    def place_marker(self, part_pos, slot_pos):
        """Place marker on the board without moving parts"""
        # Check if game is already over
        if self.winner is not None:
            return False

        # Check if inputs are valid
        if not self._validate_part_and_slot(part_pos, slot_pos):
            return False

        # Place marker
        return self.board.place_marker(part_pos, slot_pos, self.current_player)

    def move_part(self, part_pos, target_pos):

        """Move a part after the marker has been placed"""
        # Check if game is already over
        if self.winner is not None:
            return False, "Game already over"

        # Check if the target position is valid
        if not self._validate_target(target_pos, part_pos):
            return False, "Invalid target position"

        # Move part
        if not self.board.move_part(part_pos, target_pos):
            return False, "Invalid part movement"

        # Record the board state
        board_str = self.board.str_board_history()
        self.game_history.append([board_str, 0])  # Initial grade is 0

        return True, "Move successful"

    def undo_marker_placement(self, part_pos, slot_pos):
        """Undo a marker placement"""
        # Check if part exists
        if self.board.board[part_pos[0]][part_pos[1]] is None:
            return False

        # Reset the slot to empty
        self.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] = 0
        return True

    def get_current_player_object(self):
        return self.player1 if self.current_player == 1 else self.player2

    def make_move(self, part_pos, slot_pos, target_pos):
        """
        Performs a full turn: place marker and move part, then switches player if game not over.
        """
        # Get current player marker (int: 1 or 2)
        marker = self.current_player
        # Place marker
        marker_placed = self.board.place_marker(part_pos, slot_pos, marker)
        if not marker_placed:
            return False, "Invalid marker placement", None

        # Move part
        part_moved = self.board.move_part(part_pos, target_pos)
        if not part_moved:
            # Undo marker placement
            self.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] = 0
            return False, "Invalid part movement", None

        # Check for winner
        winner = self.board.is_winner(marker)
        if winner:
            self.winner = marker
            self._update_grades(marker)
            self._update_stats(marker)
            return True, "Game over", marker

        # Check for tie
        if self.board.is_tie():
            self.winner = 0
            self._update_grades(0)
            self._update_stats(0)
            return True, "Game is a tie", 0

        # Always switch to next player after a successful move!
        self.switch_player()
        print("DEBUG: After make_move, current_player is:", self.current_player)
        return True, "Move successful", None

    def _validate_part_and_slot(self, part_pos, slot_pos):
        """Validate part position and slot position"""
        # Check if part position is within bounds
        row, col = part_pos
        if not (0 <= row < 3 and 0 <= col < 3):
            print("Part position out of bounds")
            return False

        # Check if part exists
        if self.board.board[part_pos[0]][part_pos[1]] is None:
            print("Part does not exist at this position")
            return False

        # Check if slot position is within bounds
        row, col = slot_pos
        if not (0 <= row < 2 and 0 <= col < 2):
            print("Slot position out of bounds")
            return False

        # Check if slot is empty
        if self.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] != 0:
            print("Slot is already occupied")
            return False

        return True

    def _validate_target(self, target_pos, part_pos):
        """Validate target position for movement"""
        # Check if target position is within bounds
        row, col = target_pos
        if not (0 <= row < 3 and 0 <= col < 3):
            return False

        # Check if target position is empty
        if self.board.board[target_pos[0]][target_pos[1]] is not None:
            return False

        # Check if target position is different from part position
        if target_pos == part_pos:
            return False

        # Check if part can move from target_pos to part_pos
        if not self.board.can_part_move(part_pos, target_pos):
            return False

        return True

    def check_game_over(self):
        """Check for game over conditions"""
        # Check if current player won
        if self.board.is_winner(self.current_player):
            self.winner = self.current_player
            self._update_grades(self.current_player)
            self._update_stats(self.current_player)
            return True

        # Check if board is full (tie)
        if self.board.is_full():
            self.winner = 0  # 0 represents a tie
            self._update_grades(0)
            self._update_stats(0)
            return True

        return False

    def _update_grades(self, result):
        """Update the grades for game history (for AI learning)"""
        self.game_history.reverse()
        if result == 1:  # Blue wins
            for i in range(len(self.game_history)):
                self.game_history[i][1] = 1.0 * self.gamma ** i
        elif result == 2:  # Red wins
            for i in range(len(self.game_history)):
                self.game_history[i][1] = -1.0 * self.gamma ** i
        else:  # Tie
            for i in range(len(self.game_history)):
                self.game_history[i][1] = 0.0

    def _update_stats(self, winner):
        """Update game statistics"""
        if winner == 1:
            self.stats["blue_wins"] += 1
        elif winner == 2:
            self.stats["red_wins"] += 1
        else:
            self.stats["draws"] += 1

        self.save_game_stats()

    def get_smart_move(self):
        """Get move from AI player"""
        if self.winner is not None:
            return None, None, None

        current_player = self.get_current_player_object()
        if hasattr(current_player, 'get_player_move'):
            try:
                return current_player.get_player_move()
            except Exception as e:
                print(f"Error getting AI move: {str(e)}")
                return None, None, None

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

    def get_board_state(self):
        """Return a representation of the board for the view"""
        board_state = []
        for row in range(3):
            board_row = []
            for col in range(3):
                part = self.board.board[row][col]
                if part is None:
                    board_row.append(None)
                else:
                    slots = []
                    for slot_row in range(2):
                        for slot_col in range(2):
                            slots.append(part.slots[slot_row][slot_col])
                    board_row.append(slots)
            board_state.append(board_row)

        return board_state

    def load_game_stats(self, filename="game_stats.json"):
        """Load game statistics from file"""
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    self.stats = json.load(file)
            else:
                self.stats = {"blue_wins": 0, "red_wins": 0, "draws": 0}
        except Exception as e:
            print(f"Error loading game stats: {str(e)}")
            self.stats = {"blue_wins": 0, "red_wins": 0, "draws": 0}

    def save_game_stats(self, filename="game_stats.json"):
        """Save game statistics to file"""
        try:
            with open(filename, "w") as file:
                json.dump(self.stats, file)
        except Exception as e:
            print(f"Error saving game stats: {str(e)}")