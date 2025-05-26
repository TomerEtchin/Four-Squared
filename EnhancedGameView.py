import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import os


class EnhancedGameView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.master.title("4^2")
        self.master.geometry("700x750")
        self.master.configure(bg="#f0f0f0")

        # Define color scheme
        self.colors = {
            "bg": "#f0f0f0",
            "primary": "#3498db",  # Blue
            "secondary": "#e74c3c",  # Red
            "accent": "#2ecc71",  # Green
            "light": "#ecf0f1",
            "dark": "#34495e"
        }

        # Setup custom styles
        self.setup_styles()

        # Create frames
        self.create_header_frame()
        self.create_home_screen()
        self.create_game_screen()

        # Start with home screen
        self.show_home_screen()

        # Initialize game state variables
        self.current_selection = None  # Selected part position
        self.current_slot = None  # Selected slot position
        self.part_filled = False  # Track if a part has been filled this turn
        self.target_selection = None  # Selected target for movement

    def setup_styles(self):
        """Set up custom styles for widgets"""
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.colors["bg"])
        self.style.configure("TLabel", background=self.colors["bg"], font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 11))
        self.style.configure("Header.TLabel", font=("Helvetica", 18, "bold"))
        self.style.configure("Title.TLabel", font=("Helvetica", 24, "bold"))

        # Button styles
        self.style.configure("Blue.TButton", foreground="white", background=self.colors["primary"])
        self.style.configure("Red.TButton", foreground="white", background=self.colors["secondary"])
        self.style.configure("Green.TButton", foreground="white", background=self.colors["accent"])

        # Game piece styles
        self.style.configure("Blue.GamePiece.TButton", font=("Helvetica", 14, "bold"), foreground="blue")
        self.style.configure("Red.GamePiece.TButton", font=("Helvetica", 14, "bold"), foreground="red")
        self.style.configure("Empty.GamePiece.TButton", font=("Helvetica", 14))
        self.style.configure("Selected.TFrame", background="#ffe066", relief=tk.RIDGE)
        self.style.configure("Target.TFrame", background="#66ff66", relief=tk.RIDGE)
        self.style.configure("Normal.TFrame", background=self.colors["light"], relief=tk.GROOVE)

    def create_header_frame(self):
        """Create the header frame with title and logo"""
        self.frame_header = ttk.Frame(self.master, padding=10, style="TFrame")
        self.frame_header.pack(fill=tk.X)

        # Add logo if available
        try:
            logo_path = "logo.png"
            if os.path.exists(logo_path):
                image = Image.open(logo_path).resize((60, 60))
                self.logo = ImageTk.PhotoImage(image)
                self.logo_label = ttk.Label(self.frame_header, image=self.logo, style="TLabel")
                self.logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception:
            # Create text logo instead
            logo_label = ttk.Label(self.frame_header, text="SBG",
                                   font=("Helvetica", 22, "bold"),
                                   foreground=self.colors["primary"],
                                   style="TLabel")
            logo_label.pack(side=tk.LEFT, padx=(0, 10))

        self.title_label = ttk.Label(self.frame_header, text="4^2",
                                     style="Title.TLabel")
        self.title_label.pack(side=tk.LEFT)

    def create_home_screen(self):
        """Create the home screen with game options"""
        self.frame_home = ttk.Frame(self.master, padding=20, style="TFrame")

        # Welcome message
        welcome_label = ttk.Label(self.frame_home,
                                  text="Welcome to 4^2!",
                                  style="Header.TLabel")
        welcome_label.pack(pady=(0, 20))

        # Game description
        desc_text = ("A strategy game where you place markers and move board parts.\n"
                     "Form a square of four markers to win!")
        desc_label = ttk.Label(self.frame_home, text=desc_text, style="TLabel")
        desc_label.pack(pady=(0, 30))

        # Player selection
        selection_frame = ttk.Frame(self.frame_home, padding=10, style="TFrame")
        selection_frame.pack(fill=tk.X, pady=(0, 20))

        # Player 1 selection
        player1_frame = ttk.LabelFrame(selection_frame, text="Player 1 (Blue)", padding=10)
        player1_frame.pack(fill=tk.X, pady=10)

        self.player1_type = tk.IntVar(value=1)  # Default to Human
        ttk.Radiobutton(player1_frame, text="Human", variable=self.player1_type, value=1).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(player1_frame, text="Random AI", variable=self.player1_type, value=2).pack(side=tk.LEFT,
                                                                                                   padx=10)
        ttk.Radiobutton(player1_frame, text="Smart AI", variable=self.player1_type, value=3).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(player1_frame, text="AI Agent", variable=self.player1_type, value=4).pack(side=tk.LEFT, padx=10)

        # Player 2 selection
        player2_frame = ttk.LabelFrame(selection_frame, text="Player 2 (Red)", padding=10)
        player2_frame.pack(fill=tk.X, pady=10)

        self.player2_type = tk.IntVar(value=3)  # Default to Smart AI
        ttk.Radiobutton(player2_frame, text="Human", variable=self.player2_type, value=1).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(player2_frame, text="Random AI", variable=self.player2_type, value=2).pack(side=tk.LEFT,
                                                                                                   padx=10)
        ttk.Radiobutton(player2_frame, text="Smart AI", variable=self.player2_type, value=3).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(player2_frame, text="AI Agent", variable=self.player2_type, value=4).pack(side=tk.LEFT, padx=10)

        # Buttons frame
        buttons_frame = ttk.Frame(self.frame_home, padding=10, style="TFrame")
        buttons_frame.pack(fill=tk.X, pady=20)

        # Rules button
        rules_button = ttk.Button(buttons_frame, text="Game Rules",
                                  command=self.show_rules, width=15)
        rules_button.pack(side=tk.LEFT, padx=10)

        # Start game button
        start_button = ttk.Button(buttons_frame, text="Start Game",
                                  command=self.start_game, width=15)
        start_button.pack(side=tk.RIGHT, padx=10)

    def create_game_screen(self):
        """Create the game screen with board and controls"""
        self.frame_game = ttk.Frame(self.master, padding=10, style="TFrame")

        # Top controls
        self.create_top_controls()

        # Game board
        self.create_game_board()

        # Info panel
        self.create_info_panel()

    def create_top_controls(self):
        """Create top control panel for game screen"""
        top_frame = ttk.Frame(self.frame_game, padding=5, style="TFrame")
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # Back to home button
        back_button = ttk.Button(top_frame, text="← Back",
                                 command=self.show_home_screen, width=10)
        back_button.pack(side=tk.LEFT)

        # Reset button
        reset_button = ttk.Button(top_frame, text="New Game",
                                  command=self.new_game, width=10)
        reset_button.pack(side=tk.RIGHT)

    def create_game_board(self):
        """Create the game board"""
        self.frame_board_container = ttk.Frame(self.frame_game, padding=10, style="TFrame")
        self.frame_board_container.pack(padx=10, pady=10)

        # Main board frame with a border
        self.frame_board = ttk.Frame(self.frame_board_container, borderwidth=3, relief=tk.RIDGE)
        self.frame_board.pack(padx=10, pady=10)

        # Create empty board
        self.board_parts = []
        for row in range(3):
            part_row = []
            for col in range(3):
                # Skip the middle position
                if row == 1 and col == 1:
                    part_row.append(None)
                    continue

                # Create frame for this board part with a distinctive border
                part_frame = ttk.Frame(self.frame_board, borderwidth=3,
                                       relief=tk.GROOVE, style="Normal.TFrame")
                part_frame.grid(row=row, column=col, padx=3, pady=3)
                part_frame.bind("<Button-1>", lambda e, r=row, c=col: self.board_part_clicked(r, c))

                # Create slots within this part
                slots = []
                for slot_row in range(2):
                    for slot_col in range(2):
                        def make_slot_callback(r, c, sr, sc):
                            return lambda: self.slot_clicked(r, c, sr, sc)

                        slot = ttk.Button(part_frame, width=5, text='')
                        slot.grid(row=slot_row, column=slot_col, padx=2, pady=2)
                        slot.configure(command=make_slot_callback(row, col, slot_row, slot_col))
                        slots.append(slot)

                part_row.append({
                    'frame': part_frame,
                    'slots': slots
                })
            self.board_parts.append(part_row)

        # Create empty spot in middle with visual indicator
        self.middle_frame = ttk.Frame(self.frame_board, width=100, height=100,
                                      style="TFrame", borderwidth=2, relief=tk.SUNKEN)
        self.middle_frame.grid(row=1, column=1, padx=3, pady=3)
        empty_label = ttk.Label(self.middle_frame, text="Empty\nSpace",
                                foreground="gray", style="TLabel")
        empty_label.pack(expand=True, fill="both")

    def create_info_panel(self):
        """Create the information and control panel"""
        self.frame_info = ttk.Frame(self.frame_game, padding=10, style="TFrame")
        self.frame_info.pack(fill=tk.X, padx=10, pady=5)

        # Game status panel
        status_frame = ttk.LabelFrame(self.frame_info, text="Game Status", padding=10)
        status_frame.pack(fill=tk.X, pady=5)

        # Current turn indicator
        turn_frame = ttk.Frame(status_frame, style="TFrame")
        turn_frame.pack(fill=tk.X, pady=5)

        self.turn_label = ttk.Label(turn_frame, text="Current Turn:", style="TLabel")
        self.turn_label.pack(side=tk.LEFT, padx=5)

        self.turn_value = ttk.Label(turn_frame, text="Blue",
                                    foreground="blue", font=("Helvetica", 14, "bold"),
                                    style="TLabel")
        self.turn_value.pack(side=tk.LEFT, padx=5)

        # Score display
        score_frame = ttk.Frame(status_frame, style="TFrame")
        score_frame.pack(fill=tk.X, pady=5)

        self.score_label = ttk.Label(score_frame, text="Score:", style="TLabel")
        self.score_label.pack(side=tk.LEFT, padx=5)

        self.score_value = ttk.Label(score_frame, text="Blue: 0, Red: 0, Draws: 0", style="TLabel")
        self.score_value.pack(side=tk.LEFT, padx=5)

        # Status message
        self.status_var = tk.StringVar(value="Welcome to 4^2!")
        self.status = ttk.Label(self.frame_info, textvariable=self.status_var,
                                font=("Helvetica", 11, "italic"), style="TLabel")
        self.status.pack(pady=10)

        # Move controls frame
        self.move_controls = ttk.LabelFrame(self.frame_info, text="Move Controls", padding=10)
        self.move_controls.pack(fill=tk.X, pady=5)


        # Instructions
        instr_text = "1. Click a slot to place your marker\n" + \
                     "2. Click a different part to select as target for movement"
        instr_label = ttk.Label(self.move_controls, text=instr_text, style="TLabel")
        instr_label.pack(pady=5)

        # Cancel selection button
        self.cancel_button = ttk.Button(self.move_controls, text="Cancel Selection",
                                        command=self.cancel_selection, state=tk.DISABLED)
        self.cancel_button.pack(pady=5)

        # Move the BoardPart
        self.move_button = ttk.Button(self.move_controls, text="Move Selected Part",
                                      command=self.move_selected_part, state=tk.DISABLED)
        self.move_button.pack(pady=5)

    def show_home_screen(self):
        """Show the home screen and hide game screen"""
        self.frame_game.pack_forget()
        self.frame_home.pack(expand=True, fill=tk.BOTH)

    def show_game_screen(self):
        """Show the game screen and hide home screen"""
        self.frame_home.pack_forget()
        self.frame_game.pack(expand=True, fill=tk.BOTH)

    def start_game(self):
        """Start a new game with selected players"""
        self.show_game_screen()
        self.new_game()

    def new_game(self):
        """Start a new game"""
        # Setup new game in controller
        move_result = self.controller.setup_new_game(
            self.player1_type.get(),
            self.player2_type.get()
        )

        # Reset view state
        self.reset_board_view()
        self.update_turn_display()
        self.update_stats_display()
        self.current_selection = None
        self.current_slot = None
        self.target_selection = None
        self.part_filled = False
        self.cancel_button.configure(state=tk.DISABLED)
        self.status_var.set("Game started! Blue's turn.")

        # If AI goes first, process its move
        if move_result and move_result[0]:
            self.process_smart_move(move_result[1], move_result[2])

    def reset_board_view(self):
        """Reset the board view to empty state"""
        for row in range(3):
            for col in range(3):
                if row == 1 and col == 1:
                    continue  # Skip middle

                part = self.board_parts[row][col]
                for i, slot in enumerate(part['slots']):
                    slot.configure(text='', style='TButton')

                # Reset frame appearance
                part['frame'].configure(style="Normal.TFrame")

    def show_rules(self):
        """Display the game rules"""
        rules_text = """
Game Rules:

1. The game is played on a 3x3 grid of board parts, with the center space empty.
   Each board part contains a 2x2 grid of slots.

2. Players take turns. On your turn, you must:
   - Place your marker in an empty slot on any board part
   - Then move a DIFFERENT board part (not the one you placed your marker on) 
     into the empty space

3. Board parts can only move horizontally or vertically into the empty space.

4. The goal is to create a 2x2 square of your markers. This can be:
   - All 4 slots in a single board part
   - 4 adjacent slots across 2-4 different board parts

5. The game ends when a player forms a square or the board is full (draw).

Strategy tips:
- Block your opponent from forming squares
- Position your markers to create multiple winning opportunities
- Control the movement of board parts to set up future moves
"""

        # Create a custom dialog for rules
        rules_dialog = tk.Toplevel(self.master)
        rules_dialog.title("Game Rules")
        rules_dialog.geometry("500x550")
        rules_dialog.transient(self.master)
        rules_dialog.grab_set()
        rules_dialog.configure(bg=self.colors["bg"])

        # Add header
        header_frame = ttk.Frame(rules_dialog, style="TFrame", padding=10)
        header_frame.pack(fill=tk.X)

        header_label = ttk.Label(header_frame, text="S4^2 - Rules",
                                 font=("Helvetica", 16, "bold"), style="TLabel")
        header_label.pack()

        # Add rules text
        text_frame = ttk.Frame(rules_dialog, style="TFrame", padding=15)
        text_frame.pack(expand=True, fill=tk.BOTH)

        # Using Text widget for better formatting control
        rules_text_widget = tk.Text(text_frame, wrap=tk.WORD, width=50, height=20,
                                    font=("Helvetica", 11), bg=self.colors["light"])
        rules_text_widget.insert("1.0", rules_text)
        rules_text_widget.configure(state="disabled")  # Make read-only

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=rules_text_widget.yview)
        rules_text_widget.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        rules_text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Add close button
        button_frame = ttk.Frame(rules_dialog, style="TFrame", padding=15)
        button_frame.pack(fill=tk.X)

        close_button = ttk.Button(button_frame, text="Close",
                                  command=rules_dialog.destroy, width=15)
        close_button.pack(pady=5)

    def update_board_from_state(self):
        """Update the board display from the current model state."""
        board_state = self.controller.get_board_state()

        new_board_parts = [[None for _ in range(3)] for _ in range(3)]
        moved_view = None

        # Remove any part that has moved (board_state has None where a part was)
        for r in range(3):
            for c in range(3):
                if board_state[r][c] is None and self.board_parts[r][c] is not None:
                    moved_view = self.board_parts[r][c]
                    moved_view['frame'].grid_remove()  # remove from old location
                    self.board_parts[r][c] = None

        # Add parts to their new locations and update slot markers
        for r in range(3):
            for c in range(3):
                part_state = board_state[r][c]
                if part_state is not None:
                    if self.board_parts[r][c] is not None:
                        part_view = self.board_parts[r][c]
                    elif moved_view is not None:
                        part_view = moved_view
                        moved_view = None
                        # **Rebind slot button commands to new part coordinates (r, c)**
                        for i, slot_button in enumerate(part_view['slots']):
                            sr = i // 2  # slot_row (0 or 1)
                            sc = i % 2  # slot_col (0 or 1)
                            slot_button.configure(
                                command=lambda r=r, c=c, sr=sr, sc=sc: self.slot_clicked(r, c, sr, sc)
                            )
                    else:
                        continue

                    # Place the part’s frame in the new location
                    part_view['frame'].grid(row=r, column=c)
                    # Update each slot’s display (B, R, or empty) based on part_state
                    for i, marker in enumerate(part_state):
                        slot_btn = part_view['slots'][i]
                        if marker == 1:
                            slot_btn.configure(text='B', style='Blue.GamePiece.TButton')
                        elif marker == 2:
                            slot_btn.configure(text='R', style='Red.GamePiece.TButton')
                        else:
                            slot_btn.configure(text='', style='Empty.GamePiece.TButton')

                    new_board_parts[r][c] = part_view

        # Replace the old board_parts with the updated one
        self.board_parts = new_board_parts

        # Update the empty space indicator (middle_frame) to the current empty position
        empty_pos = self.find_empty_space()
        if empty_pos is not None:
            self.middle_frame.grid_remove()
            self.middle_frame.grid(row=empty_pos[0], column=empty_pos[1])

    def update_turn_display(self):
        """Update the turn indicator"""
        current_player = self.controller.get_current_player()
        if current_player == 1:
            self.turn_value.configure(text="Blue", foreground="blue")
        else:
            self.turn_value.configure(text="Red", foreground="red")

    def update_stats_display(self):
        """Update the game statistics display"""
        stats = self.controller.get_game_stats()
        self.score_value.configure(
            text=f"Blue: {stats['blue_wins']}, Red: {stats['red_wins']}, Draws: {stats['draws']}"
        )

    def cancel_selection(self):
        """Cancel the current marker placement and selection"""
        if self.part_filled and self.current_selection:
            # Reset only if we've placed a marker but not moved yet
            part_pos = self.current_selection
            slot_pos = self.current_slot

            # Undo the marker placement in the model
            self.controller.model.board.board[part_pos[0]][part_pos[1]].slots[slot_pos[0]][slot_pos[1]] = 0

            # Reset selection state
            self.reset_selection_state()
            self.update_board_from_state()
            self.status_var.set("Selection canceled. Place your marker again.")

    def reset_selection_state(self):
        """Reset the current selection state"""
        self.part_filled = False
        self.current_selection = None
        self.current_slot = None
        self.target_selection = None
        self.reset_highlights()
        self.cancel_button.configure(state=tk.DISABLED)
        self.move_button.configure(state=tk.DISABLED)

    def smart_turn(self):
        """Handle AI's turn"""
        move_result = self.controller.get_smart_move()
        if move_result and move_result[0]:
            part_pos, slot_pos, target_pos = move_result[1]
            self.process_smart_move(part_pos, slot_pos, target_pos)

    def get_valid_parts_to_move(self):
        """Return parts that can move into current empty space"""
        valid_parts = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        empty_r, empty_c = self.find_empty_space()

        for dr, dc in directions:
            r, c = empty_r + dr, empty_c + dc
            if 0 <= r < 3 and 0 <= c < 3:
                part = self.board_parts[r][c]
                if part is not None:
                    valid_parts.append((r, c))

        return valid_parts

    def reset_highlights(self):
        """Reset all highlighting on the board."""
        for row in range(3):
            for col in range(3):
                if self.board_parts[row][col] is not None:
                    self.board_parts[row][col]['frame'].configure(style="Normal.TFrame")

    def highlight_possible_targets(self, part_pos):
        """Highlight possible target positions for movement."""
        targets = self.controller.get_possible_targets(part_pos)

        self.reset_highlights()

        self.board_parts[part_pos[0]][part_pos[1]]['frame'].configure(style="Selected.TFrame")

        for row, col in targets:
            if self.board_parts[row][col] is not None:
                self.board_parts[row][col]['frame'].configure(style="Target.TFrame")

    def board_part_clicked(self, row, col):
        """Handle when a board part (frame) is clicked"""
        if not self.part_filled:
            return  # Cannot move unless a marker is placed

        valid_parts = self.get_valid_parts_to_move()
        if (row, col) not in valid_parts:
            self.status_var.set("Selected part is not adjacent to the empty space.")
            return

        # Save selected target
        self.target_selection = (row, col)

        # Highlight target
        self.reset_highlights()
        self.highlight_possible_targets(self.current_selection)
        if row != 1 or col != 1:
            self.board_parts[row][col]['frame'].configure(style="Selected.TFrame")

        self.move_button.configure(state=tk.NORMAL)
        self.status_var.set("Ready to move! Click 'Move Selected Part'.")

    def slot_clicked(self, part_row, part_col, slot_row, slot_col):
        """Handle a slot being clicked"""
        # Get current player
        current_player = self.controller.get_current_player()

        # Check if game is already over
        if self.controller.get_winner() is not None:
            self.status_var.set("Game is over. Start a new game.")
            return

        # Check if it's human's turn based on player type settings
        is_human_turn = False
        if current_player == 1 and self.player1_type.get() == 1:
            is_human_turn = True
        elif current_player == 2 and self.player2_type.get() == 1:
            is_human_turn = True

        if not is_human_turn:
            self.status_var.set("Not your turn!")
            return

        # If we haven't selected a part for our marker yet
        if not self.part_filled:
            part_pos = (part_row, part_col)
            slot_pos = (slot_row, slot_col)

            # Check if this slot is empty
            board_state = self.controller.get_board_state()
            if board_state[part_row][part_col] is None:
                self.status_var.set("Invalid selection!")
                return

            slot_index = slot_row * 2 + slot_col
            if board_state[part_row][part_col][slot_index] != 0:
                self.status_var.set("This slot is already occupied!")
                return


            # Place marker in the model (don't move part yet)
            success = self.controller.model.board.place_marker(part_pos, slot_pos, current_player)
            if not success:
                self.status_var.set("Invalid marker placement!")
                return

            # Remember our selection for when we select a part to move next
            self.current_selection = part_pos
            self.current_slot = slot_pos
            self.part_filled = True

            # Update the view to show the placed marker
            self.update_board_from_state()

            # Highlight this part to show it's selected
            self.board_parts[part_row][part_col]['frame'].configure(style="Selected.TFrame")

            # Show possible targets for next move
            self.highlight_possible_targets(part_pos)

            # Enable cancel button
            self.cancel_button.configure(state=tk.NORMAL)

            # Update status
            player_color = "Blue" if current_player == 1 else "Red"
            self.status_var.set(f"{player_color} marker placed. Now select a different part to move.")

        # If we've already placed a marker and now we're selecting a part to move
        else:
            # Check if this is our target selection (a part to move, not a slot)
            target_pos = (part_row, part_col)

            # Can't select the same part where we placed our marker
            if target_pos == self.current_selection:
                self.status_var.set("You can't move the same part where you placed your marker")
                return

            # Check if this is a valid target
            targets = self.controller.get_possible_targets(self.current_selection)
            if target_pos not in targets:
                self.status_var.set("Invalid target! Select a highlighted part.")
                return

            # This is our target part to move
            self.target_selection = target_pos

            # Make the move through the controller
            success, result, winner = self.controller.make_move(
                self.current_selection,  # Where we placed marker
                self.current_slot,  # Which slot in the part
                self.target_selection  # Which part to move
            )

            # Reset selection state
            self.reset_selection_state()

            if not success:
                # Show error message
                self.status_var.set(f"Invalid move: {result}")
                return

            # Update the board view
            self.update_board_from_state()

            # Check for winner
            if winner is not None:
                self.game_over(winner)
                return

            # Update turn indicator
            self.update_turn_display()
            self.status_var.set(f"{'Red' if self.controller.get_current_player() == 2 else 'Blue'}'s turn")

            # If next player is AI, make its move
            if (self.controller.get_current_player() == 1 and self.player1_type.get() != 1) or \
                    (self.controller.get_current_player() == 2 and self.player2_type.get() != 1):
                self.master.after(500, self.make_smart_move)

    def move_selected_part(self):
        """Move the selected board part."""
        if not self.target_selection:
            self.status_var.set("No target part selected.")
            return

        empty_pos = self.find_empty_space()
        success, message, winner, smart_result = self.controller.move_part_only(
            self.target_selection, empty_pos
        )

        if not success:
            self.status_var.set(f"Invalid move: {message}")
            self.update_board_from_state()
            self.reset_selection_state()
            return

        self.reset_selection_state()
        self.update_board_from_state()

        if winner is not None:
            self.game_over(winner)
            return

        self.update_turn_display()
        self.status_var.set(f"{'Red' if self.controller.get_current_player() == 2 else 'Blue'}'s turn")

        current_player_type = self.controller.model.get_current_player_type()
        if current_player_type in [2, 3]:
            self.master.after(500, self.smart_turn)

    def make_smart_move(self):
        """Trigger AI to make a move"""
        success, move_info, winner = self.controller.get_smart_move()

        if success:
            self.process_smart_move(move_info, winner)
        else:
            self.status_var.set(f"AI error: {move_info}")

    def find_empty_space(self):
        """Return (row, col) of the empty space"""
        board_state = self.controller.get_board_state()

        for row in range(3):
            for col in range(3):
                if board_state[row][col] is None:
                    return (row, col)

        return None  # Should never happen

    def process_smart_move(self, move_info, winner):
        """Process a move made by AI"""
        if not isinstance(move_info, tuple):
            return

        # Visualize AI's move
        part_pos, slot_pos, target_pos = move_info
        player = self.controller.get_current_player()
        player_name = "Blue" if player == 1 else "Red"

        # First highlight the part where AI placed marker
        self.board_parts[part_pos[0]][part_pos[1]]['frame'].configure(style="Selected.TFrame")
        self.master.update()
        self.master.after(300)  # Brief pause

        # Then highlight the part AI is moving
        if self.board_parts[target_pos[0]][target_pos[1]]:
            self.board_parts[target_pos[0]][target_pos[1]]['frame'].configure(style="Target.TFrame")
            self.master.update()
            self.master.after(300)  # Brief pause

        # Update the board view
        self.update_board_from_state()
        self.reset_highlights()

        # Show AI's move in status
        self.status_var.set(f"{player_name} AI moved: Placed marker at position {part_pos}, slot {slot_pos} " +
                            f"and moved part at {target_pos}")

        # Check for winner
        if winner is not None:
            self.game_over(winner)
            return

        # Update turn indicator
        self.update_turn_display()

        # If next player is also AI, make its move after a delay
        if (self.controller.get_current_player() == 1 and self.player1_type.get() != 1) or \
                (self.controller.get_current_player() == 2 and self.player2_type.get() != 1):
            self.master.after(800, self.make_smart_move)
        winner = self.controller.get_winner()
        if winner is not None:
            self.game_over(winner)

    def game_over(self, winner):
        """Handle game over state"""
        self.update_stats_display()

        if winner == 1:
            self.status_var.set("Game over! Blue wins!")
            messagebox.showinfo("Game Over", "Blue wins!")
        elif winner == 2:
            self.status_var.set("Game over! Red wins!")
            messagebox.showinfo("Game Over", "Red wins!")
        else:
            self.status_var.set("Game over! It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")


# Main application entry point
def main():
    root = tk.Tk()
    root.configure(bg="#f0f0f0")

    # Set application icon if available
    try:
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass  # Skip if icon not available

    # Create model and controller
    from GameModel import GameModel
    from GameController import GameController

    model = GameModel()
    controller = GameController(model)
    view = EnhancedGameView(root, controller)

    root.mainloop()


if __name__ == "__main__":
    main()