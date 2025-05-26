class GameController:
    def __init__(self, model):
        self.model = model

    def setup_new_game(self, player1_type, player2_type):
        """Setup a new game with specified player types"""
        self.model.reset_game()
        self.model.setup_players(player1_type, player2_type)

        # If player 1 is AI, make its first move automatically
        if player1_type in [2, 3, 4]:  # Random or Smart AI
            return self.get_smart_move()
        return None, None, None

    def make_move(self, part_pos, slot_pos, target_pos):
        """Process a player's move"""
        # First place the marker
        marker_success = self.model.place_marker(part_pos, slot_pos)
        if not marker_success:
            print(f"Failed to place marker at part {part_pos}, slot {slot_pos}")
            return False, "Invalid marker placement", None

        # Then move the part
        move_success, message = self.model.move_part(part_pos, target_pos)
        if not move_success:
            # Undo the marker placement
            self.model.undo_marker_placement(part_pos, slot_pos)
            print(f"Failed to move part from {target_pos} to {part_pos}: {message}")
            return False, message, None

        # Check if the game is over after this move
        self.model.check_game_over()
        winner = self.model.winner

        # If no winner, switch players
        if winner is None:
            self.model.switch_player()

        return True, "Move successful", winner

    def place_marker_only(self, part_pos, slot_pos):
        """Place a marker without moving a part"""
        success = self.model.place_marker(part_pos, slot_pos)
        return success

    def move_part_only(self, part_pos, target_pos):
        """Move a part after marker has been placed"""
        success, message = self.model.move_part(part_pos, target_pos)
        if success:
            self.model.check_game_over()
            winner = self.model.winner

            if winner is None:
                self.model.switch_player()

                current_player_type = self.model.get_current_player_type()
                if current_player_type in [2, 3, 4]:
                    smart_result = self.get_smart_move()
                    return success, message, winner, smart_result[1:]

            return success, message, winner, None
        else:
            return success, message, None, None

    def get_ai_move(self):
        """
        Handles the AI player's move, whether Random, Smart, or AI Agent.
        """
        current_player = self.model.get_current_player()
        move = current_player.get_player_move()
        if move is None:
            return False, "AI could not make a move.", None
        part_pos, slot_pos, target_pos = move
        success, message, winner = self.model.make_move(part_pos, slot_pos, target_pos)
        return success, (part_pos, slot_pos, target_pos), winner

    def get_smart_move(self):
        """Get and process a move from the AI player"""
        part_pos, slot_pos, target_pos = self.model.get_smart_move()

        if part_pos is None or slot_pos is None or target_pos is None:
            return False, "AI couldn't find a valid move", None

        marker_success = self.model.place_marker(part_pos, slot_pos)
        if not marker_success:
            return False, "AI couldn't place marker", None

        move_success, message = self.model.move_part(part_pos, target_pos)
        if not move_success:
            self.model.undo_marker_placement(part_pos, slot_pos)
            return False, "AI couldn't move part", None

        self.model.check_game_over()
        winner = self.model.winner

        if winner is None:
            self.model.switch_player()

        return True, (part_pos, slot_pos, target_pos), winner

    def get_board_state(self):
        """Get the current board state"""
        return self.model.get_board_state()

    def get_possible_targets(self, part_pos):
        """Get possible target positions for a part"""
        return self.model.get_possible_targets(part_pos)

    def get_current_player(self):
        """Get the current player number"""
        return self.model.current_player

    def get_winner(self):
        """Get the current winner (if any)"""
        return self.model.winner

    def get_game_stats(self):
        """Get game statistics"""
        return self.model.stats

    def undo_marker_placement(self, part_pos, slot_pos):
        """Undo a marker placement"""
        self.model.undo_marker_placement(part_pos, slot_pos)