import numpy as np
import copy
from tensorflow.keras.models import load_model
from Player import Player

class AiAgent(Player):
    def __init__(self, board, marker):
        super().__init__(board, marker)
        self.model = load_model('ann_model.keras')

    def get_all_legal_moves(self):
        moves = []
        # Find the empty space first
        empty_pos = None
        for i in range(3):
            for j in range(3):
                if self.board.board[i][j] is None:
                    empty_pos = (i, j)
                    break
            if empty_pos:
                break

        if empty_pos is None:
            print("DEBUG: No empty space found on board")
            return moves

        empty_row, empty_col = empty_pos

        # For each part on the board
        for i in range(3):
            for j in range(3):
                if self.board.board[i][j] is None:
                    continue
                # Only consider parts adjacent to the empty space
                if (abs(i - empty_row) == 1 and j == empty_col) or (abs(j - empty_col) == 1 and i == empty_row):
                    # For each empty slot in the part
                    for k in range(2):
                        for l in range(2):
                            if self.board.board[i][j].slots[k][l] == 0:
                                moves.append(((i, j), (k, l), empty_pos))
        return moves

    def encode_board(self, board=None):
        """
        Encode the current board into a numpy array suitable for the model.
        """
        if board is None:
            board = self.board
        key = board.str_board_history()
        features = []
        for ch in key:
            if ch == '0':
                features.append(0)
            elif ch == '1':
                features.append(1)
            elif ch == '2':
                features.append(2)
            elif ch == 'X':
                features.append(-1)

        return features

    def get_player_move(self):
        print("DEBUG: AiAgent.get_player_move called")
        possible_moves = self.get_all_legal_moves()
        best_score = -float('inf')
        best_move = None

        for move in possible_moves:
            part, slot, target = move
            # Work on a copy of the board to avoid corrupting real game state
            board_copy = copy.deepcopy(self.board)

            marker_placed = board_copy.place_marker(part, slot, self.marker)
            part_moved = board_copy.move_part(part, target)

            if not marker_placed or not part_moved:
                continue  # Skip illegal moves

            # Encode and predict
            input_array = np.array([self.encode_board(board_copy)], dtype=float)
            try:
                pred = self.model.predict(input_array, verbose=0)
                print(
                    f"DEBUG: prediction raw output: {pred}, shape: {getattr(pred, 'shape', type(pred))}")  # Print prediction for debugging
                score = float(np.array(pred).flatten()[0])  # Guaranteed to work for any shape
            except Exception as e:
                print(f"Model prediction error: {e}")
                continue

            if score > best_score:
                best_score = score
                best_move = move

        if best_move is not None:
            print("DEBUG: AiAgent returning move:", best_move)
            return best_move

        print("DEBUG: AiAgent could not generate a valid move!")
        # Fallback: choose any legal move if available, or pass
        return possible_moves[0] if possible_moves else (None, None, None)
