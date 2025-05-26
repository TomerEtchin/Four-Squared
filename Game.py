from Board import Board
from SmartAgent import SmartAgent


# Constants for grading
WIN_GRADE = 1.0
LOSE_GRADE = -1.0
DRAW_GRADE = 0.0


class Game:
    def __init__(self, player1_type: int, player2_type: int, gamma: float) -> None:
        self.board = Board()

        # Setup players
        if player1_type == 1:  # Human
            from HumanPlayer import HumanPlayer
            self.player1 = HumanPlayer(self.board, 1)  # Blue
        elif player1_type == 2:  # Random
            from RandomPlayer import RandomPlayer
            self.player1 = RandomPlayer(self.board, 1)
        elif player1_type == 3:  # Smart
            self.player1 = SmartAgent(self.board, 1)

        if player2_type == 1:  # Human
            from HumanPlayer import HumanPlayer
            self.player2 = HumanPlayer(self.board, 2)  # Red
        elif player2_type == 2:  # Random
            from RandomPlayer import RandomPlayer
            self.player2 = RandomPlayer(self.board, 2)
        elif player2_type == 3:  # Smart
            self.player2 = SmartAgent(self.board, 2)
        elif player2_type == 4:
            from AIAgent import AIAgent
            self.player2 = AIAgent(self.board, 2)

        self.current_player = 1  # Blue starts
        self.game_history = []
        self.gamma = gamma

    def play_game(self):
        # Continue until board is full or someone wins
        while not self.board.is_full() and not self.board.is_winner(1) and not self.board.is_winner(2):
            print(f"\nPlayer {self.current_player}'s turn")
           # self.board.print_board()

            # Get the current player
            current_player_obj = self.player1 if self.current_player == 1 else self.player2

            # Get move
            try:
                # For any player type, get_player_move should return part_pos, slot_pos, target_pos
                part_pos, slot_pos, target_pos = current_player_obj.get_player_move()

                if part_pos is None or slot_pos is None or target_pos is None:
                    print("No valid moves left")
                    break

                # Place marker
                self.board.place_marker(part_pos, slot_pos, self.current_player)

                # Move a different part - not the one where marker was placed
                # This check ensures the player is following the rules
                if part_pos == target_pos:
                    print("Error: Cannot move the same part where marker was placed!")
                    # Undo the marker placement and try again
                    self.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] = 0
                    continue

                # Move part
                self.board.move_part(part_pos, target_pos)


                # Record the board state in game history
                board_str = self.board.str_board_history()
                self.game_history.append([board_str, 0])  # Initial grade is 0

                # Check if current player won after this move
                if self.board.is_winner(self.current_player):
                    print(f"Player {self.current_player} wins!")
                   # self.board.print_board()
                    self.update_grades(self.current_player)
                    return self.current_player, self.game_history

                # Check if board is full
                if self.board.is_full():
                    print("Game ended in a tie")
                   # self.board.print_board()
                    self.update_grades(0)
                    return 0, self.game_history

                # Switch players
                self.current_player = 2 if self.current_player == 1 else 1

            except Exception as e:
                print(f"Error during move: {str(e)}")
                import traceback
                traceback.print_exc()  # This will print the full error traceback
                break

        # Final board state
        #self.board.print_board()

        # Check game result
        if self.board.is_winner(1):
            print("Player 1 (Blue) wins!")
            self.update_grades(1)
            return 1, self.game_history
        elif self.board.is_winner(2):
            print("Player 2 (Red) wins!")
            self.update_grades(2)
            return 2, self.game_history
        else:
            print("Game ended in a tie")
            self.update_grades(0)
            return 0, self.game_history

    # Updates the grades for game_history
    def update_grades(self, result):
        self.game_history.reverse()
        if result == 1:  # Blue wins
            for i in range(len(self.game_history)):
                self.game_history[i][1] = WIN_GRADE * self.gamma ** i
        elif result == 2:  # Red wins
            for i in range(len(self.game_history)):
                self.game_history[i][1] = LOSE_GRADE * self.gamma ** i
        else:  # Tie
            for i in range(len(self.game_history)):
                self.game_history[i][1] = DRAW_GRADE * self.gamma ** i