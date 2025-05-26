from Player import Player
import random
import os
import json
from Board import Board


class SmartAgent(Player):
    def __init__(self, board: Board, marker):
        Player.__init__(self, board, marker=marker)
        self.opponent_marker = 2 if marker == 1 else 1
        self.max_depth = 3  # Limit search depth due to complexity
        self.position_scores = {}  # Initialize the dictionary

    def get_player_move(self):
        print(f"Player {self.marker} (Smart Agent) is thinking...")
        best_score = float('-inf')
        best_move = None
        best_target = None

        empty_places = self.board.get_empty_places()
        if not empty_places:
            return None, None, None  # Fixed: Return three None values

        # For each possible placement
        for part_pos, slot_pos in empty_places:
            # Get possible movements after placing
            possible_targets = self.get_possible_targets(part_pos)

            # Skip if no possible targets
            if not possible_targets:
                continue

            # For each possible movement
            for target_pos in possible_targets:
                # Try this move
                self.board.place_marker(part_pos, slot_pos, self.marker)

                # Check if this is a winning move (no need to continue if so)
                if self.board.is_winner(self.marker):
                    # Undo move for evaluation
                    self.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] = 0
                    print(f"Found winning move: Place at {part_pos},{slot_pos} then move to {target_pos}")
                    return (part_pos, slot_pos, target_pos)

                # If not immediately winning, move the part
                original_part = self.board.board[part_pos[0]][part_pos[1]]
                self.board.move_part(part_pos, target_pos)

                # Evaluate with minimax
                score = self.minimax(0, False, float('-inf'), float('inf'))

                # Undo the part movement
                self.board.board[target_pos[0]][target_pos[1]] = None
                self.board.board[part_pos[0]][part_pos[1]] = original_part

                # Undo the marker placement
                self.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] = 0

                # Update best move
                if score > best_score:
                    best_score = score
                    best_move = (part_pos, slot_pos)
                    best_target = target_pos

        if best_move is None:
            # Fallback to random move if no good move found
            valid_moves = []
            for part_pos, slot_pos in empty_places:
                targets = self.get_possible_targets(part_pos)
                if targets:  # Only add if there are valid targets
                    for target_pos in targets:
                        valid_moves.append((part_pos, slot_pos, target_pos))

            if not valid_moves:
                return None, None, None  # No valid moves available

            # Choose a random valid move
            random_move = random.choice(valid_moves)
            return random_move[0], random_move[1], random_move[2]

        print(f"AI chose move: Place at {best_move} then move part to {best_target}")
        return best_move[0], best_move[1], best_target

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

    def minimax(self, depth, is_maximizing, alpha, beta):
        # Check for terminal states
        if self.board.is_winner(self.marker):
            return 100 - depth
        elif self.board.is_winner(self.opponent_marker):
            return depth - 100
        elif self.board.is_full() or depth >= self.max_depth:
            return self.evaluate_board()

        # Get all possible moves
        empty_places = self.board.get_empty_places()
        if not empty_places:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for part_pos, slot_pos in empty_places:
                possible_targets = self.get_possible_targets(part_pos)
                for target_pos in possible_targets:
                    # Make the move
                    self.board.place_marker(part_pos, slot_pos, self.marker)
                    original_part = self.board.board[part_pos[0]][part_pos[1]]
                    self.board.move_part(part_pos, target_pos)

                    # Evaluate
                    score = self.minimax(depth + 1, False, alpha, beta)

                    # Undo the move
                    self.board.board[target_pos[0]][target_pos[1]] = None
                    self.board.board[part_pos[0]][part_pos[1]] = original_part
                    self.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] = 0

                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for part_pos, slot_pos in empty_places:
                possible_targets = self.get_possible_targets(part_pos)
                for target_pos in possible_targets:
                    # Make the move
                    self.board.place_marker(part_pos, slot_pos, self.opponent_marker)
                    original_part = self.board.board[part_pos[0]][part_pos[1]]
                    self.board.move_part(part_pos, target_pos)

                    # Evaluate
                    score = self.minimax(depth + 1, True, alpha, beta)

                    # Undo the move
                    self.board.board[target_pos[0]][target_pos[1]] = None
                    self.board.board[part_pos[0]][part_pos[1]] = original_part
                    self.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] = 0

                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score

    def evaluate_board(self):
        """Heuristic evaluation function for the current board state"""
        score = 0

        # Check for potential winning patterns
        # First check for 3 markers in a row within a part
        for row in range(3):
            for col in range(3):
                part = self.board.board[row][col]
                if part is not None:
                    # Count markers in this part
                    my_markers = 0
                    opponent_markers = 0
                    for r in range(2):
                        for c in range(2):
                            if part.slots[r][c] == self.marker:
                                my_markers += 1
                            elif part.slots[r][c] == self.opponent_marker:
                                opponent_markers += 1

                    # Award points based on marker dominance
                    if my_markers == 3:
                        score += 5  # Almost winning
                    elif my_markers == 2 and opponent_markers == 0:
                        score += 2  # Good position
                    elif opponent_markers == 3:
                        score -= 5  # Opponent almost winning
                    elif opponent_markers == 2 and my_markers == 0:
                        score -= 2  # Opponent good position

        # Check for potential connections between parts
        # This is simplified - for a full evaluation we'd need to check all winning patterns

        return score

    def get_position_key(self):
        """Get a unique key for the current board position"""
        return self.board.str_board_history()

    def store_position_score(self, position_key, score):
        """Store a score for a given position"""
        self.position_scores[position_key] = score

    def get_position_score(self, position_key):
        """Get the stored score for a position if available"""
        return self.position_scores.get(position_key)

    def load_position_scores(self, filename="agent_positions.json"):
        """Load previously saved positions and scores"""
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    self.position_scores = json.load(file)
                    print(f"Loaded {len(self.position_scores)} positions from {filename}")
            else:
                print(f"No position file found at {filename}, starting with empty dictionary")
        except Exception as e:
            print(f"Error loading positions: {str(e)}")
            self.position_scores = {}

    def save_position_scores(self, filename="agent_positions.json"):
        """Save position evaluations to file"""
        try:
            with open(filename, "w") as file:
                json.dump(self.position_scores, file)
                print(f"Saved {len(self.position_scores)} positions to {filename}")
        except Exception as e:
            print(f"Error saving positions: {str(e)}")