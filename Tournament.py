import json
import os
from Game import Game
class Tournament:
    def __init__(self, player1_type: int, player2_type: int, num_games: int, gamma: float, json_file_name=None):
        self.player1_type = player1_type
        self.player2_type = player2_type
        self.num_games = num_games
        self.results = {'1': 0, '2': 0, '0': 0}  # Wins for player 1, player 2, and ties
        self.gamma = gamma
        self.QTable = self.load_scoreboard(json_file_name)

    def start_tournament(self):
        for game_num in range(self.num_games):
            print(f"\n=== Starting Game {game_num + 1}/{self.num_games} ===")
            game = Game(self.player1_type, self.player2_type, self.gamma)
            result, history = game.play_game()
            self.results[str(result)] += 1

            # Update QTable with game history
            for board, grade in history:
                if board in self.QTable:
                    # Update existing entry
                    current_grade, count = self.QTable[board]
                    new_grade = (current_grade * count + grade) / (count + 1)
                    self.QTable[board] = (new_grade, count + 1)
                else:
                    # Create new entry
                    self.QTable[board] = (grade, 1)

            # Save after each game to avoid losing data
            if game_num % 5 == 0:
                self.save_scoreboard("Board-QTable.json")

        # Final save and print results
        self.save_scoreboard("Board-QTable.json")
        self.print_results()

    def print_results(self):
        tie_count = self.results['0']
        player1_count = self.results['1']
        player2_count = self.results['2']
        print("\n=== Tournament Results ===")
        print(f"Games played: {self.num_games}")
        print(f"Player 1 (Blue) won: {player1_count} games ({player1_count / self.num_games * 100:.1f}%)")
        print(f"Player 2 (Red) won: {player2_count} games ({player2_count / self.num_games * 100:.1f}%)")
        print(f"Ties: {tie_count} games ({tie_count / self.num_games * 100:.1f}%)")

    def load_scoreboard(self, json_file_name=None):
        """Loads the QTable from a json file"""
        if json_file_name is None:
            print("No file specified. Starting with an empty QTable")
            return {}

        if os.path.exists(json_file_name):
            try:
                with open(json_file_name, "r") as file:
                    dictionary = json.load(file)
                    print(f"QTable loaded from {json_file_name}")
                    return dictionary
            except Exception as e:
                print(f"Error loading QTable: {str(e)}")
                return {}
        else:
            print(f"File {json_file_name} not found. Starting with an empty QTable")
            return {}

    def save_scoreboard(self, filename="Board-QTable.json"):
        """Saves the QTable to a json file"""
        try:
            with open(filename, "w") as file:
                json.dump(self.QTable, file)
                print(f"QTable saved to {filename}")
        except Exception as e:
            print(f"Error saving QTable: {str(e)}")

    # Example of running a tournament


if __name__ == "__main__":
    # Player types: 1=Human, 2=Random, 3=Smart
    tournament = Tournament(
        player1_type=3,  # SmartAgent for player 1 (Blue)
        player2_type=2,  # Random for player 2 (Red)
        num_games = 10000,
        gamma=0.9,
        json_file_name="Board-QTable.json"
    )
    tournament.start_tournament()