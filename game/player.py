import subprocess
import json
import time

class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def get_move(self, board_state, time_limit=None):
        raise NotImplementedError


class HumanPlayer(Player):
    def __init__(self, name, player_id):
        super().__init__(name, player_id)
        
        
class ExecutableBot(Player):
    def __init__(self, name, player_id, path, time_limit=2.0):
        super().__init__(name, player_id)
        self.path = path
        self.time_limit = time_limit  # seconds

    def get_move(self, board_state):
        try:
            input_data = {
                "board": board_state,
                "player_id": self.player_id,
                "time_limit": int(self.time_limit * 1000)  # milliseconds
            }
            start_time = time.time()

            result = subprocess.run(
                [self.path],
                input=json.dumps(input_data),
                capture_output=True,
                text=True,
                timeout=self.time_limit
            )

            elapsed = time.time() - start_time
            move = int(result.stdout.strip())
            return move

        except subprocess.TimeoutExpired:
            print(f"Bot {self.name} exceeded time limit!")
            return 0  # fallback move

        except Exception as e:
            print(f"Error running bot {self.name}: {e}")
            return 0  # fallback